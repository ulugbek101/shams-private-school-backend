# Generated by Django 4.2.4 on 2023-08-10 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_rename_month_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.BigIntegerField(null=True),
        ),
    ]
