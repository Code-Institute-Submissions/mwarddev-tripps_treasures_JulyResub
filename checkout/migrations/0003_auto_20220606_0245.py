# Generated by Django 3.2 on 2022-06-06 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_purchaseitem_personalise'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='customise',
            field=models.TextField(default='None'),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='upload_images',
            field=models.ImageField(blank=True, null=True, upload_to='customer_images'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='personalise',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
