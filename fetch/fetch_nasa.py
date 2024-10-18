import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_nasa():
    try:
        response = requests.get(
            f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA')}"
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return f"Pavadinimas: {data['title']}\nNuoroda: {data['url']}"

        return data
    except requests.RequestException as e:
        print(f"Error fetching NASA data: {e}")
        sys.exit(1)


def main():
    fetch_nasa()


if __name__ == "__main__":
    main()
