# Generated by Django 4.0.3 on 2022-03-15 11:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_order_order_id_billingaddress_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=uuid.UUID('a63f44b6-3309-4236-8651-2576f5a15848'), max_length=100),
        ),
    ]
