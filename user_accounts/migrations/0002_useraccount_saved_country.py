# Generated by Django 3.2 on 2022-06-05 13:59

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='saved_country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]