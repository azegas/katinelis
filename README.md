# Katinelis

This repo was made by duplicating [this MM2 repo at this time](https://github.com/azegas/mm2/tree/e526029dbc7a5c8f6cc1cc5abc02875324583419)

Monitor was ditched, since there was a need for it and mm2 could no longer be used. But what will we try to accomplish in this app is:

- fetch sensor data - display as morning message in telegram
- fetch cvbankas data - display as morning message in telegram
- fetch random quote - display as morning message in telegram
- motion sensor detects movement - sends alarm to telegram
- have an option to fetch needed info at any time
- vix kasdien tikrinti

## Install rasberry OS

Use `Raspberry pi imager` bla.

For options:

```bash
sudo raspi-config
```

## Environment

```
mkdir ~/venvs
cd ~/venvs
python -m venv venv-katinelis
source ~/venvs/venv-katinelis/bin/activate
mkdir ~/GIT
cd ~/GIT
git clone git@github.com:azegas/katinelis.git
cd ~/GIT/katinelis
pip install -r requirements.txt
```

Put into `.bashrc`, so environment is always activated:

```
vim ~/.bashrc

# add these to the bottom of the file:
source ~/venvs/venv-katinelis/bin/activate
source ~/GIT/katinelis/.env
cd ~/GIT/katinelis
```




## Stocks

For stock historical data, can use this free api - https://www.alphavantage.co/documentation/

But for live data - wont work, premium feature

## About telegram

Go to Telegram app on phone or on windows app and search for the `BotFather`.

Use the command `/newbot` to create a new bot and get your BOT_TOKEN.

For CHAT_ID - Open Telegram and search for your bot using its username (the one you created with BotFather).
Start a chat with your bot by sending any message (e.g., "Hello").

Then visit bot api link - `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

Look for the chat object in the JSON response. Your `CHAT_ID` will be listed there, typically as `chat.id`.

Use it for things.

To use the bot in the GROUP chat, add the bot to the group chat as a member. Write any message into the chat, navigate to the bot api link like we did above,
there you should see the chatid of a group chat (starts with -, must be added to .env with ''). 

Now you should be able to send messages to the group chat.

Simple app example:

```py
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DIR = os.getenv("BASE_DIR")


def main():
    send_message("hello")


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)


if __name__ == "__main__":
    main()
```

Can also create shortcuts so user does not have to type the commands you want. Go to BotFather, choose `/setcommands` and write such commands:

```
labas - labas ir info
citke - citata
tempe - temperatura + dregme kiuciu chatoj
jobs - cvbankas vadovo darbai
```

So now when someone is interacting wiht the bot, it can write `/` to see all the commands, and then pick a particular one, for example `/labas`.

## About all the services

## About cronjobs

```bash
# crontab -l > cron.txt
# crontab cron.txt
# crontab -e
# crontab -

# dont use $USER - it will not find the user... at least did not bother to find how to make it work. .bashrc?

# Explanation of the cron job syntax:
# * * * * * command
# | | | | |
# | | | | +---- Day of the week (0 - 7) (Sunday = 0 or 7)
# | | | +------ Month (1 - 12)
# | | +-------- Day of the month (1 - 31)
# | +---------- Hour (0 - 23)
# +------------ Minute (0 - 59)
```

## Start chromium automatically by default

`start_chromium.sh` file.

## About services

```bash
# This service file runs the humidity sensor script as a systemd service
# It ensures the script starts automatically on boot and restarts if it crashes

chmod +x /home/arvypi/GIT/katinelis/fetches/pi_humidity.py
sudo vi /etc/systemd/system/humidity-sensor.service
sudo cp /home/arvypi/GIT/katinelis/services/humidity-sensor.service /etc/systemd/system/humidity-sensor.service

sudo systemctl daemon-reload
sudo systemctl start humidity-sensor.service
sudo systemctl status humidity-sensor.service
sudo systemctl stop humidity-sensor.service
sudo journalctl -u humidity-sensor.service -f
sudo systemctl enable humidity-sensor.service

IF THE SERVICE IS NOT WORKING, TRY THE FOLLOWING:
sudo systemctl stop humidity-sensor.service
sudo systemctl disable humidity-sensor.service
sudo rm /etc/systemd/system/humidity-sensor.service
sudo systemctl daemon-reload
sudo systemctl reset-failed humidity-sensor.service
```

# Docs

## packages

`source ~/venvs/venv-mm2/bin/activate`

```sh
# web app
pip install flask flask-socketio python-dotenv beautifulsoup4 requests
# humidity sensor
pip install adafruit-circuitpython-dht
# raspberry system info
pip install psutil gpiozero
```

## ssh

Connect to pi from windows:
```pwsh
ssh arvypi@raspberrypi.local
# or:
ssh arvypi@192.168.0.82
```

TTransfer files from local directory to raspberry - `tranfer.bat`

## crontab

# crontab -l > cron.txt
# crontab cron.txt
# crontab -e
# crontab -l

## Humidity sensor

# humidity_pi

```sh
arvypi@raspberrypi:~ $ cat /proc/cpuinfo | grep Model
Model           : Raspberry Pi 3 Model B Rev 1.2
```

Pin info - https://i.pinimg.com/736x/bf/e5/02/bfe502b80a3248ed48fb125182235c32.jpg

-----------------

## Humidity sensor

I have humidity sensor and I want to read the humidity from it and print it to the console.

I want to do this every second. my sensor is DHT22 - https://www.anodas.lt/dht22-temperaturos-ir-dregmes-jutiklis-su-pcb

```
Temperature: 25.5°C, Humidity: 67.2%
Temperature: 25.5°C, Humidity: 67.1%
Temperature: 25.5°C, Humidity: 67.1%
Temperature: 25.5°C, Humidity: 67.2%
Temperature: 25.5°C, Humidity: 67.2%
Temperature: 25.5°C, Humidity: 66.9%
Temperature: 25.5°C, Humidity: 66.9%
Temperature: 25.5°C, Humidity: 67.6%
Temperature: 25.5°C, Humidity: 67.6%
```

## motion sensor

I have such motion sensor - https://www.anodas.lt/hc-sr501-pir-judesio-daviklis?search=PIR

its pins - https://images.theengineeringprojects.com/image/main/2019/01/Introduction-to-HC-SR501.jpg

- TODO try to control delay
- TODO try to control sensitivity

# How it works with socket.io

Backend:
- continuous process on the backend to fetch the data (cronjob)
- cronjob fetches every minute or so during 05:00 - 07:00 and 17:00 - 22:00
- when the cron job finished, usually it stores the results in a .json file

Frontend:
- on the frontend, we have a flask app
- flask app in itself has some socketio functions that READ data from the files
- We tell, with the help of javascript, how often to read the data of those files and then update the page with it

## Adding new service step by step

`app.py` - backend, server (provides data, ways to read the data(connections to connect to))
`static/js/main.js` - frontend, client (requests data)

### Create a script that is running in the backend and fetches data, saves the results to a file

### Create a way to read the data from the file `read_cvbankas_data`:

```python
def read_cvbankas_data():
    file_path = os.path.join(base_dir, "data/data_cvbankas.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    return {"error": "Data not found"}
```

### Schedule that script to run periodically (and periodically save the data to the file)

Update cronjob file or create a system service to run the script periodically.