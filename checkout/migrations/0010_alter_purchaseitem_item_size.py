# Generated by Django 3.2 on 2022-06-27 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_remove_purchase_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='item_size',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
