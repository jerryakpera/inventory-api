"""
This file is used to configure the app name for the suppliers app.
"""

from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    """
    This class is used to configure the app name for the suppliers app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.suppliers"
