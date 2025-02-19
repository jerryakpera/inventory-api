# Generated by Django 5.1.1 on 2025-02-19 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0011_productvariant_sku"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productvariant",
            name="sku",
            field=models.CharField(
                default="TEMP-SKU",
                editable=False,
                help_text="Stock Keeping Unit for inventory tracking.",
                max_length=30,
                unique=True,
            ),
            preserve_default=False,
        ),
    ]
