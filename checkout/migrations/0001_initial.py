# Generated by Django 3.2 on 2022-06-02 20:53

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_accounts', '0001_initial'),
        ('treasures', '0001_initial'),
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_number', models.CharField(editable=False, max_length=50)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=50)),
                ('county', models.CharField(blank=True, max_length=100, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('postcode', models.CharField(max_length=20)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('gift_wrapped', models.BooleanField(blank=True, default=False, null=True)),
                ('gift_message', models.TextField()),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('original_basket', models.TextField(default='')),
                ('stripe_pid', models.CharField(default='', max_length=254)),
                ('purchase_status', models.CharField(choices=[('new', 'New Order'), ('in_prod', 'In Production'), ('prod_comp', 'Production Complete'), ('despd', 'Despatched')], default='new', max_length=9)),
                ('shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping', to='shipping.shipping')),
                ('user_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to='user_accounts.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_size', models.CharField(blank=True, max_length=7, null=True)),
                ('qty', models.IntegerField(default=0)),
                ('item_total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchaseitems', to='checkout.purchase')),
                ('treasure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treasures.treasure')),
            ],
        ),
    ]
