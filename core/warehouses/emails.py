"""
Emails functions for the `core` app.
"""

from django.template.loader import render_to_string

from core.custom_user.models import User
from core.warehouses.models import Stock
from core.warehouses.tasks import send_email_task


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

    html_message = render_to_string(
        "warehouses/emails/low_stock_alert.html",
        context,
    )

    for recipient_email in recipients:
        send_email_task.delay(
            email=recipient_email,
            subject=subject,
            html_message=html_message,
        )
