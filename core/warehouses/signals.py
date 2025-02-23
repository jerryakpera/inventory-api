"""
Signals for the warehouses app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .emails import send_low_stock_alert
from .models import StockAlert, WarehouseUser


@receiver(post_save, sender=StockAlert)
def send_low_stock_email(sender, instance, created, **kwargs):  # pragma: no cover
    """
    Send an email to the warehouse managers when a stock alert is created.

    Parameters
    ----------
    sender : StockAlert
        The StockAlert model.
    instance : StockAlert
        The StockAlert instance.
    created : bool
        Whether the instance was created or updated.
    **kwargs
        Additional keyword arguments.
    """

    if created:
        warehouse_managers = WarehouseUser.objects.filter(
            warehouse=instance.stock.warehouse,
            role=WarehouseUser.RoleChoices.MANAGER,
        ).select_related("user")

        emails = [
            manager.user.email for manager in warehouse_managers if manager.user.email
        ]

        if emails:
            send_low_stock_alert(instance.stock, emails)
