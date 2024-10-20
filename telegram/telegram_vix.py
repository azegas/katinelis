import os
import json
import requests
from dotenv import load_dotenv
import sys

from fetch.fetch_vix import fetch_vix

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")

# Add the parent directory to sys.path (for log_config)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def send_vix_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)


def message_vix():
    data = fetch_vix()
    print(data)
    return send_vix_to_telegram(data)
