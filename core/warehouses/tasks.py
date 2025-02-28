"""
Tasks for the `accounts` app.
"""

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail

from celery import shared_task
from core.products.models import Product


@shared_task(name="send_email_task")
def send_email_task(email, subject, html_message):  # pragma: no cover
    """
    Send a message to the email in a separate thread.

    This function handles sending an email with the provided subject and HTML content
    to the email address.

    Parameters
    ----------
    email : str
        The email address to which the message will be sent.
    subject : str
        The subject of the email.
    html_message : str
        The HTML content of the email.

    Returns
    -------
    str
        The email address to which the message will be sent.
    """

    send_mail(
        subject=subject,
        message="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
    )

    return email
