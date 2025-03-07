"""
Django management command to create a superuser if none exists.
"""

from decouple import config
from django.core.management.base import BaseCommand

from core.custom_user.models import User


class Command(BaseCommand):
    """
    Create a superuser if none exist.

    Example:
        manage.py createsuperuser_if_none_exists --user=admin --password=changeme
    """

    def handle(self, *args, **options):
        """
        Handle the command execution.

        Checks for existing superusers. If none are found, it creates a new superuser
        using email and password from the environment variables. Outputs a confirmation
        message indicating the creation of the superuser.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to the command.
        **options : dict
            Keyword arguments passed to the command.
        """

        if User.objects.exists():
            return

        email = config("SU_EMAIL")
        password = config("SU_PASSWORD")

        User.objects.create_superuser(
            email=email,
            password=password,
        )

        self.stdout.write(f'User "{email}" was created')
