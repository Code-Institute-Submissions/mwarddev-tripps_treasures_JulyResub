# Generated by Django 3.2 on 2022-06-06 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treasures', '0006_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treasure',
            name='uploadable_images',
        ),
    ]
