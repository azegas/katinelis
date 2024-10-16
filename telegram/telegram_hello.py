import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")


def message_hello():
    message = "Labas, sveiki atvyke. Cia rasite ta ir ana. Noredami bla, rasykite '/' ir pasirinkite viena is pasirinkciu bla."
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    requests.post(url, data=payload)
