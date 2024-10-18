import os
import requests
from datetime import datetime, timedelta


def fetch_weather():
    # Get today's date
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    # Make the API request to fetch weather data for today
    api_url = f"https://api.meteo.lt/v1/stations/panevezio-ams/observations/{date_str}"
    response = requests.get(api_url)
    data_fetched_from_api = response.json()

    # Retrieve the observation for 06:00 am from the fetched data and return only airTemperature
    desired_observation = None
    for observation in data_fetched_from_api["observations"]:
        if observation["observationTimeUtc"] == f"{date_str} 06:00:00":
            desired_observation = observation["airTemperature"]
            break
    if desired_observation is None:
        return None
    return desired_observation


def main():
    weather = fetch_weather()


if __name__ == "__main__":
    main()
