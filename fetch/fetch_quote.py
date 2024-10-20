import requests
import ssl
import json
import os
from datetime import datetime
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_config import logger

load_dotenv()


def fetch_quote():
    url = "https://api.quotable.io/random"
    try:
        # Create a custom SSL context that doesn't verify certificates
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Suppress the InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning
        )

        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return f'"{data["content"]}" - {data["author"]}'
    except requests.RequestException as e:
        print(f"Error fetching quote: {e}")
        return {
            "content": "An error occurred while fetching the quote.",
            "author": "Unknown",
        }


if __name__ == "__main__":
    # Suppress the InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )
    quote = fetch_quote()
    print(f"Quote: {quote}")
