# Generated by Django 3.2 on 2022-06-02 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('saved_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('saved_address_line1', models.CharField(blank=True, max_length=100, null=True)),
                ('saved_address_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('saved_city', models.CharField(blank=True, max_length=50, null=True)),
                ('saved_county', models.CharField(blank=True, max_length=100, null=True)),
                ('saved_postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]