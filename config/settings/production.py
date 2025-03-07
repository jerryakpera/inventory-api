"""
Settings to be used in production environment.
"""

from datetime import timedelta

import dj_database_url
from decouple import config

from .base import *
from .base import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASES["default"] = dj_database_url.parse(config("DATABASE_URL"))
