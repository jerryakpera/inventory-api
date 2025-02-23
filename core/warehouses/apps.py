"""
App configuration for `warehouses` app.
"""

from django.apps import AppConfig


class WarehousesConfig(AppConfig):
    """
    Configuration class for the `warehouses` app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.warehouses"

    def ready(self):
        """
        Import signals.
        """
        import core.warehouses.signals
