# Generated by Django 5.1.1 on 2025-02-21 04:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("warehouses", "0003_warehouseuser"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="warehouseuser",
            unique_together={("user", "warehouse")},
        ),
    ]
