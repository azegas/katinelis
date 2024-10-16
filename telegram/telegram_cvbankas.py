import os
import json
import requests
from dotenv import load_dotenv
import sys

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")

# Add the parent directory to sys.path (for log_config)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_cvbankas_data():
    file_path = os.path.join(BASE_DIR, "data/data_cvbankas.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            if "jobs" in data and isinstance(data["jobs"], list):
                data["jobs"] = data["jobs"][:3]
            return data
    return {"error": "Data not found"}


def send_cvbankas_to_telegram(data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Format the job data into a message
    if "jobs" in data and isinstance(data["jobs"], list):
        message = "Latest Job Listings:\n\n"
        for job in data["jobs"]:
            message += f"Title: {job['title']}\n"
            message += f"Company: {job['company']}\n"
            message += f"Salary: {job['salary']}\n"
            message += f"City: {job['city']}\n"
            message += f"Posted: {job['job_posted']}\n"
            message += f"Href: {job['href']}\n\n"
    else:
        message = "No job listings available."

    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


def message_cvbankas():
    data = get_cvbankas_data()
    return send_cvbankas_to_telegram(data)
