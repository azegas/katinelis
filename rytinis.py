import json
import requests
import os
from dotenv import load_dotenv
import schedule
from time import sleep
from telegram.telegram_cvbankas import message_cvbankas
from telegram.telegram_sensor import read_sensor_data
from datetime import datetime
from fetch.fetch_weather import fetch_weather
from fetch.fetch_nasa import fetch_nasa
from fetch.fetch_quote import fetch_quote
from fetch.fetch_vix import fetch_vix


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
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        print("fsio haraso, issisiunte rytine")
    except requests.RequestException as e:
        print(f"Error sending message: {e}")


def process():
    combined_message = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Labas rytas! ☀️😙\n\n"
        f"{fetch_vix()}\n\n"
        f"Orelis Kiūčiuose: \n\n"
        f"{fetch_weather()}\n"
        f"{read_sensor_data()}\n\n"
        f"Dienos citata: \n\n"
        f"{fetch_quote()}\n\n"
        f"Dienos NASA paveiksliukas: \n\n"
        f"{fetch_nasa()}\n\n"
    )
    message_rytine(combined_message)
    message_rytine(
        f"Vadovas darbeliai nuo 3000eur:\n\n"
        f"{message_cvbankas(keyword='vadovas', pages=5, salary=3000, filter_to=10)}"
    )


def main():

    # process()

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
