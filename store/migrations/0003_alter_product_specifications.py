# Generated by Django 4.2.16 on 2025-02-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_specifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='specifications',
            field=models.TextField(blank=True, default=''),
        ),
    ]
