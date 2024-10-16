import json
import requests
import os
from dotenv import load_dotenv
import schedule
from time import sleep
from telegram.telegram_cvbankas import message_cvbankas
from telegram.telegram_quote import get_quote_data
from telegram.telegram_sensor import get_sensor_data
from datetime import datetime


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")


def message_rytine(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    requests.post(url, data=payload)


def process():
    combined_message = (
        f"Labas rytas! ☀️😙\n\n"
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Orelis Kiuciu name: \n\n"
        f"{get_sensor_data()}\n\n"
        f"Dienos citata: \n\n"
        f"{get_quote_data()}\n\n"
    )
    message_rytine(combined_message)


def main():

    process()

    SCHEDULE_TIME = "07:00"

    print("App started...")
    print(f"Scheduled to run at {SCHEDULE_TIME}")

    schedule.every(900).seconds.do(lambda: print("I'm alive"))
    schedule.every().day.at(SCHEDULE_TIME).do(lambda: process())

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
