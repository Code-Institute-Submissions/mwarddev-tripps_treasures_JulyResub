# Generated by Django 3.2 on 2022-06-02 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier_name', models.CharField(max_length=50)),
                ('courier_descripton', models.TextField()),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
    ]
