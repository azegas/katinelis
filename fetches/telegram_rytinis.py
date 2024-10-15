import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")

def get_quote():
    file_path_random_quote = os.path.join(BASE_DIR, "data/random_quote.json")
    with open(file_path_random_quote) as f:
        data = json.load(f)
        return data

def format_quote(quote_data):
    return f"Quote: {quote_data['quote']['content']}\nAuthor: {quote_data['quote']['author']}"

def send_quote_to_telegram(quote_text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': quote_text}
    requests.post(url, data=payload)
    # TODO logging

def main():
    quote_data = get_quote()
    quote_text = format_quote(quote_data)
    send_quote_to_telegram(quote_text)

if __name__ == "__main__":
    main()