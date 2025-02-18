"""
This is a simple Python client that sends a GET request to the server.
"""

import requests


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


endpoint = "https://httpbin.org/status/200/"
endpoint = "https://httpbin.org/"
endpoint = "http://localhost:8000/api/"

get_response = requests.get(endpoint, json={"query": "value"})

log_this(get_response.json())
