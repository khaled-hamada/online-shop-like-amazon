# Generated by Django 3.2.8 on 2021-11-09 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='activate',
            new_name='active',
        ),
    ]
