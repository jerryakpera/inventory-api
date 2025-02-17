"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
env = config("ENV", "production")
DEBUG = True if env == "development" else False

ALLOWED_HOSTS = config("HOSTS_ALLOWED").split(" ")


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


THIRD_PARTY_APPS = [
    "django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig",
    "core.custom_user.apps.CustomUserConfig",
    "taggit",
]


LOCAL_APPS = [
    "core.products",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "custom_user.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# STORAGES dictionary is used to configure multiple storage backends for
# different types of files.
# The 'default' storage is used for file uploads (MEDIA), while 'staticfiles'
# is used for serving static assets (CSS, JS, images).
STORAGES = {
    # The default storage backend used for handling uploaded files (MEDIA files).
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        # Files will be stored on the local filesystem.
    },
    # The storage backend used for handling static files in production.
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        # Whitenoise is used to serve compressed static files with caching
        # for better performance.
    },
}

# URL prefix used for serving static files (CSS, JavaScript, images).
# It defines where the static files will be accessible from the browser.
STATIC_URL = "static/"

# Additional directories where Django will search for static files,
# apart from the app-specific "static" directories.
# Here, we have defined that Django should look for static files in the
# "core/static" directory within the project.
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

# Directory where all static files will be collected when you run the
# `collectstatic` command.
# In production, all static files from different apps and static directories
# are collected into this folder.
STATIC_ROOT = BASE_DIR / "staticfiles"

# The file system path where uploaded media files (e.g., images, documents)
# will be stored.
# Uploaded files will be saved in the "media" directory within the project.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# URL prefix used to serve media files.
# This is the public URL where uploaded media files can be accessed from the
# browser.
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TAGGIT_CASE_INSENSITIVE = True
