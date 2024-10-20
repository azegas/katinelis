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

from fetch.fetch_cvbankas import fetch_cvbankas_jobs


def message_cvbankas(keyword, pages, salary, filter_to):
    data = fetch_cvbankas_jobs(
        keyword=keyword, pages=pages, salary=salary, filter_to=filter_to
    )

    if isinstance(data, list):
        message = ""
        for job in data:
            message += f"Title: {job['title']}\n"
            message += f"Company: {job['company']}\n"
            message += f"Salary: {job['salary']}\n"
            message += f"City: {job['city']}\n"
            message += f"Posted: {job['job_posted']}\n"
            message += f"Link: {job['href']}\n\n"
    else:
        message = "No job listings available."

    return message


if __name__ == "__main__":
    message_cvbankas(keyword="vadovas", pages=5, salary=3000, filter_to=10)
