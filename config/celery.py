"""
Celery config for project.
"""

import os

from celery import Celery
from config.settings import base

if base.DEBUG:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings.local",
    )
else:  # pragma: no cover
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings.production",
    )

app = Celery("django-celery")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)


app.autodiscover_tasks()
