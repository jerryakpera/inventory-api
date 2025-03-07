# Generated by Django 5.1.1 on 2025-02-23 19:13

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_historicalproduct_historicalproductvariant"),
        ("suppliers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsupplierproduct",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Price of the product.",
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="historicalsupplierproduct",
            name="product_variant",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="The product provided by the supplier.",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="products.productvariant",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsupplierproduct",
            name="supplier",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="Supplier who provides the product.",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="suppliers.supplier",
            ),
        ),
        migrations.AlterField(
            model_name="supplierproduct",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Price of the product.",
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="supplierproduct",
            name="product_variant",
            field=models.ForeignKey(
                help_text="The product provided by the supplier.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="suppliers",
                to="products.productvariant",
            ),
        ),
        migrations.AlterField(
            model_name="supplierproduct",
            name="supplier",
            field=models.ForeignKey(
                help_text="Supplier who provides the product.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="suppliers.supplier",
            ),
        ),
    ]
