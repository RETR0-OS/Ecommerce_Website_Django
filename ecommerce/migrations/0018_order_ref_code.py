# Generated by Django 4.0.4 on 2022-05-25 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0017_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default=1234, max_length=500),
        ),
    ]
