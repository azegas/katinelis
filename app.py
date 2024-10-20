import requests
import os
import time
from dotenv import load_dotenv
from telegram.telegram_sensor import message_sensor
from telegram.telegram_quote import message_quote
from telegram.telegram_cvbankas import message_cvbankas
from telegram.telegram_hello import message_hello
from telegram.telegram_vix import message_vix

# TODO logging to each step like in ahs. Logs for service statuses also

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 100}  # Long polling
    response = requests.get(url, params=params)
    return response.json()


"""
tempe - temperatura + dregme kiuciu chatoj
citke - citata
vix - vix skaiciukas
django - cvbankas django darbai
vadovas - cvbankas vadovo darbai
"""


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

                    if text == "/tempe@BotauskasBot" or text == "/tempe":
                        message_sensor()
                        print("response sent")

                    elif text == "/citke@BotauskasBot" or text == "/citke":
                        message_quote()
                        print("response sent")

                    elif text == "/vix@BotauskasBot" or text == "/vix":
                        message_vix()
                        print("response sent")

        time.sleep(1)  # Sleep for a second before polling again


if __name__ == "__main__":
    main()
