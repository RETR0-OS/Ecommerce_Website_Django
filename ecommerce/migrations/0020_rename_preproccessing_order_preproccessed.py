# Generated by Django 4.0.4 on 2022-05-25 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0019_alter_order_ref_code_refund'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='preproccessing',
            new_name='preproccessed',
        ),
    ]
