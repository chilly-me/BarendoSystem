# Generated by Django 4.2.16 on 2024-11-10 07:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_receipt_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receipt_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
