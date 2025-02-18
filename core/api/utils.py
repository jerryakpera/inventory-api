"""
Utility functions for the inventory API.
"""


def log_this(message, icon="📢"):
    """
    Log the message to the console.

    Parameters
    ----------
    message : str
        The message to log.
    icon : str, optional
        The icon to display before the message.
    """
    print("")
    print(icon * 5)
    print(message)
    print(icon * 5)
    print("")
