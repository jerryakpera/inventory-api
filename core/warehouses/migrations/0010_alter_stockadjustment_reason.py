# Generated by Django 5.1.1 on 2025-02-23 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouses", "0009_stockadjustment_stockaudit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stockadjustment",
            name="reason",
            field=models.CharField(
                choices=[
                    ("DAMAGE", "Damaged"),
                    ("LOSS", "Lost"),
                    ("EXPIRY", "Expired"),
                    ("AUDIT_CORRECTION", "Audit Correction"),
                ],
                default="LOSS",
                max_length=50,
            ),
        ),
    ]
