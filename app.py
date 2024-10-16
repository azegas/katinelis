"""
tempe - temperatura/dregme namuose
citke - dienos citata
"""

import requests
import os
import time
from dotenv import load_dotenv
from telegram.telegram_sensor import message_sensor
from telegram.telegram_quote import message_quote
from telegram.telegram_cvbankas import message_cvbankas

# TODO logging to each step like in ahs

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


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
                        message_sensor()
                        print("response sent")

                    elif text == "/citke":
                        message_quote()
                        print("response sent")

                    elif text == "/jobs":
                        message_cvbankas()
                        print("response sent")

        time.sleep(1)  # Sleep for a second before polling again


if __name__ == "__main__":
    main()
