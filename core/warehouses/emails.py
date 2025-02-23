"""
Emails functions for the `core` app.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.custom_user.models import User
from core.warehouses.models import Stock


def send_low_stock_alert(
    stock: Stock,
    recipients: list[User],
):
    """
    Send an email to the recipient to alert them that a product is low in stock.

    Parameters
    ----------
    stock : Stock
        The stock object.
    recipients : list[User]
        The users to send the email to.
    """
    subject = f"Low stock alert for {stock.product_variant} at {stock.warehouse}"

    context = {
        "stock": stock,
        "recipients": recipients,
    }

    html_message = render_to_string("warehouses/emails/low_stock_alert.html", context)
    plain_message = strip_tags(html_message)

    for recipient_email in recipients:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
            html_message=html_message,
        )
