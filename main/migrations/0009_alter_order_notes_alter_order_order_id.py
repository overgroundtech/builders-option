# Generated by Django 4.0.3 on 2022-04-17 15:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_order_notes_order_status_alter_order_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=uuid.UUID('deb42978-d883-4107-af66-176b69fe8019'), max_length=100),
        ),
    ]