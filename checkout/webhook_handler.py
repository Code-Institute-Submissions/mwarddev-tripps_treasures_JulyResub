from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Purchase, PurchaseItem
from treasures.models import Treasure
from user_accounts.models import UserAccount

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, purchase):
        """Send the user a confirmation email"""
        cust_email = purchase.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'purchase': purchase})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'purchase': purchase,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        print(intent)
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        account = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            account = UserAccount.objects.get(user__username=username)
            if save_info:
                account.saved_full_name = shipping_details.full_name
                account.saved_phone = shipping_details.phone
                account.saved_address_line1 = shipping_details.address.line1
                account.saved_address_line2 = shipping_details.address.line2
                account.saved_city = shipping_details.address.city
                account.saved_county = shipping_details.sddress.state
                account.saved_postcode = shipping_details.address.postal_code
                account.saved_country = shipping_details.address.country
                account.save()

        purchase_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                purchase = Purchase.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone__iexact=billing_details.phone,
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postcode__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                purchase_exists = True
                break
            except Purchase.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if purchase_exists:
            self._send_confirmation_email(purchase)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS:\
                    Verified order already in database', status=200)
        else:
            purchase = None
            try:
                purchase = Purchase.objects.create(
                    full_name=shipping_details.name,
                    user_account=account,
                    email=billing_details.email,
                    phone=shipping_details.phone,
                    address_line1=shipping_details.address.line1,
                    address_line2=shipping_details.address.line2,
                    city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    postcode=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(basket).items():
                    treasure = Treasure.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        purchase_item = PurchaseItem(
                            purchase=purchase,
                            treasure=treasure,
                            quantity=item_data,
                        )
                        purchase_item.save()
                    else:
                        for size, quantity in item_data['sizeable'].items():
                            purchase_item = PurchaseItem(
                                purchase=purchase,
                                treasure=treasure,
                                quantity=quantity,
                                treasure_size=size,
                            )
                            purchase_item.save()
            except Exception as exception:
                if purchase:
                    purchase.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR:\
                        {exception}', status=500)
        self._send_confirmation_email(purchase)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS:\
                Created purchase in webhook', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
