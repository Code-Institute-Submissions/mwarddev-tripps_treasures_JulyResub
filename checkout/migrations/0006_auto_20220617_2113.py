# Generated by Django 3.2 on 2022-06-17 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_remove_purchaseitem_upload_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='gift_message',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='gift_wrapped',
        ),
    ]