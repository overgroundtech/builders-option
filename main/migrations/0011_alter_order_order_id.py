# Generated by Django 4.0.3 on 2022-04-25 08:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=uuid.UUID('578cc8be-9b37-4055-97b6-d511778a5a80'), max_length=100),
        ),
    ]
