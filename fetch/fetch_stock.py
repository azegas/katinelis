import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# TODO fetch only specific stock, in our case - vix ir inform ar siandine good day ar ne

from config import SYMBOLS
from log_config import logger

load_dotenv()


def fetch_stock_data():
    logger.info("##########################################################")
    logger.info("Fetch stock data START")

    stock_data = {}
    fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    for symbol in SYMBOLS:
        url = f"https://finance.yahoo.com/quote/{symbol}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        price_element = soup.find("fin-streamer", {"data-testid": "qsp-price"})
        change_element = soup.find("fin-streamer", {"data-testid": "qsp-price-change"})
        change_percent_element = soup.find(
            "fin-streamer", {"data-testid": "qsp-price-change-percent"}
        )
        volume_element = soup.find(
            "fin-streamer", {"data-field": "regularMarketVolume"}
        )
        one_year_estimate_element = soup.find(
            "fin-streamer", {"data-field": "targetMeanPrice"}
        )

        stock_data[symbol] = {
            "price": (price_element.get_text(strip=True) if price_element else "N/A"),
            "change": (
                change_element.get_text(strip=True) if change_element else "N/A"
            ),
            "change_percent": (
                change_percent_element.get_text(strip=True).strip("()")
                if change_percent_element
                else "N/A"
            ),
            "volume": (
                volume_element.get_text(strip=True) if volume_element else "N/A"
            ),
            "one_year_estimate": (
                one_year_estimate_element.get_text(strip=True)
                if one_year_estimate_element
                else "N/A"
            ),
        }

        logger.info(
            "%s - fetched stock data",
            symbol,
        )

    logger.info("Fetched stock data for %s", SYMBOLS)
    logger.debug("Stock data %s", stock_data)
    save_stock_data(stock_data, fetch_time)
    logger.info("Fetched stock data END")
    return stock_data


def save_stock_data(stock_data, fetch_time):
    base_dir = os.getenv("BASE_DIR")
    file_path = os.path.join(base_dir, "data/data_stock.json")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        data_to_save = {"timestamp": fetch_time, "stocks": stock_data}
        with open(file_path, "w") as file:
            json.dump(data_to_save, file, indent=4)
        logger.info(f"Stock data saved to {file_path}")
        logger.info("Fetch stock data END")
        logger.info("##########################################################")
    except IOError as e:
        logger.error(f"Failed to save stock data: {e}")


def main():
    fetch_stock_data()


if __name__ == "__main__":
    main()
