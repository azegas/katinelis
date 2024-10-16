"""
tempe - temperatura/dregme namuose
citke - dienos citata
"""

import json
import requests
import os
import time
from dotenv import load_dotenv

# TODO logging to each step like in ahs


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")


def get_quote_data():
    file_path_random_quote = os.path.join(BASE_DIR, "data/random_quote.json")
    with open(file_path_random_quote) as f:
        data = json.load(f)
        return data


def format_quote(quote_data):
    return f"Quote: {quote_data['quote']['content']}\nAuthor: {quote_data['quote']['author']}"


def send_quote_to_telegram(quote_text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": quote_text}
    requests.post(url, data=payload)


def get_sensor_data():
    file_path_random_quote = os.path.join(BASE_DIR, "data/sensor_data.json")
    with open(file_path_random_quote) as f:
        data = json.load(f)
        return data


def format_sensor_data(sensor_data):
    return f"Temperature: {sensor_data['temperature']}\nHumidity: {sensor_data['humidity']}"


def send_sensor_data_to_telegram(sensor_text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": sensor_text}
    requests.post(url, data=payload)


def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 100}  # Long polling
    response = requests.get(url, params=params)
    return response.json()


def main():
    print("App started")
    offset = None
    while True:
        print("Pooling...")
        updates = get_updates(offset)
        for update in updates["result"]:
            # print(update)
            if "message" in update:  # Check if 'message' key exists
                message = update["message"]
                if "text" in message:  # Check if 'text' key exists
                    offset = (
                        update["update_id"] + 1
                    )  # Update offset for the next request
                    text = message["text"]
                    user = message["from"]["first_name"]

                    print(f"{user} says: {text}")  # Log the received message

                    if text == "/tempe":
                        sensor_data = get_sensor_data()
                        sensor_text = format_sensor_data(sensor_data)
                        send_sensor_data_to_telegram(sensor_text)

                    elif text == "/citke":  # Use elif to avoid checking both conditions
                        quote_data = get_quote_data()
                        quote_text = format_quote(quote_data)
                        send_quote_to_telegram(quote_text)

        time.sleep(1)  # Sleep for a second before polling again


if __name__ == "__main__":
    main()
