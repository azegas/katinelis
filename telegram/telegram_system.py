import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")


def get_system_data():
    file_path_random_quote = os.path.join(BASE_DIR, "data/data_system.json")
    with open(file_path_random_quote) as f:
        data = json.load(f)
        return f"Quote: {data['quote']['content']}\nAuthor: {data['quote']['author']}"


def send_quote_to_telegram(quote_text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": quote_text}
    requests.post(url, data=payload)


def message_quote():
    data = get_quote_data()
    return send_quote_to_telegram(data)
