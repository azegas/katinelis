import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")


def read_sensor_data():
    file_path_random_quote = os.path.join(BASE_DIR, "data/data_sensor.json")
    with open(file_path_random_quote) as f:
        data = json.load(f)
        return f"Vidus: {data['temperature']} °C, {data['humidity']} %"


def send_sensor_data_to_telegram(sensor_text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": sensor_text}
    requests.post(url, data=payload)


def message_sensor():
    data = read_sensor_data()
    return send_sensor_data_to_telegram(data)
