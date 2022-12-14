import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from treasures.models import Treasure
from user_accounts.models import UserAccount


# Order status
STATUS = (
    ('New Order', 'new_order'),
    ('In Production', 'in_production'),
    ('Production Complete', 'production_complete'),
    ('Despatched', 'despatched'),
)


class Purchase(models.Model):
    """ Model for customer purchases """
    purchase_number = models.CharField(max_length=50,
                                       null=False,
                                       editable=False)
    user_account = models.ForeignKey(UserAccount,
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='purchases')
    full_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    address_line1 = models.CharField(max_length=100, null=False, blank=False)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    county = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    purchase_date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6,
                                        decimal_places=2,
                                        null=False,
                                        default=0)
    subtotal = models.DecimalField(max_digits=6,
                                   decimal_places=2,
                                   null=False,
                                   default=0)
    grand_total = models.DecimalField(max_digits=6,
                                      decimal_places=2,
                                      null=False,
                                      default=0)
    purchase_status = models.CharField(max_length=19,
                                       choices=STATUS,
                                       default='New Order')
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254,
                                  null=False,
                                  blank=False,
                                  default='')

    class Meta:
        """
        Order the purchases
        """
        ordering = ['-purchase_date']

    def generate_purchase_number(self):
        """ Generate a unique purchase number for purchase reference """
        return uuid.uuid4().hex.upper()

    def calc_total(self):
        """
        Sum the grand total whenever a new item is
        added to or removed from the basket
        """
        self.subtotal = self.purchaseitems.aggregate(Sum('item_total'))['item_total__sum'] or 0  # noqa
        self.delivery_cost = self.subtotal * settings.DELIVERY_PERCENTAGE / 100
        self.grand_total = self.subtotal + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the save to set the purchase number
        if not already set
        """
        if not self.purchase_number:
            self.purchase_number = self.generate_purchase_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.purchase_number


class PurchaseItem(models.Model):
    """ Item info for checkout """
    purchase = models.ForeignKey(Purchase,
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE,
                                 related_name='purchaseitems')
    treasure = models.ForeignKey(Treasure,
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE)
    item_size = models.CharField(max_length=20, null=True, blank=True)
    qty = models.IntegerField(null=False, blank=False, default=0)
    customise = models.TextField(null=True, blank=True)
    personalise = models.CharField(max_length=150, null=True, blank=True)
    item_total = models.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     null=False,
                                     blank=False,
                                     editable=False)

    def save(self, *args, **kwargs):
        """
        Override save to set the item_total
        and update the subtotal
        """
        self.item_total = self.treasure.price * self.qty
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Name: {self.treasure.name} on order\
             {self.purchase.purchase_number}'
