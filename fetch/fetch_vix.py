import requests
from bs4 import BeautifulSoup


def fetch_vix():
    url = "https://tradingeconomics.com/vix:ind"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the market last value
        vix = soup.find(id="market_last").text.strip()
        if float(vix) < 20:
            return f"Vix: {vix} aka Žemėje viskas gerai!"
        elif 20 <= float(vix) <= 30:
            return f"Vix: {vix} aka Žemėje kažkas negerai!!!"
        elif float(vix) > 40:
            return f"Vix: {vix} aka Žemėje kažkas ITIN negerai!!!!!!!!!!!!!!!!!!!!!!!!!"

        # ... additional data extraction can be added here ...
    else:
        # Added debugging information
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(
            f"Response content: {response.content[:200]}"
        )  # Print first 200 characters of the response
        return None


def main():
    fetch_vix()


if __name__ == "__main__":
    main()
