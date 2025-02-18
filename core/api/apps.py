"""
This module contains the configuration for the 'core.api' application.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration for the 'core.api' application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.api"
