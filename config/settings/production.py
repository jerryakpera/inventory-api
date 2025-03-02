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

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False

CORS_ALLOWED_ORIGINS = [
    "https://inventory-app-d7569.web.app",
]
CSRF_TRUSTED_ORIGINS = [
    "https://inventory-app-d7569.web.app",
]
