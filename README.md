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

## About telegram

What the hell. Integration with telegram.

Go to Telegram and search for the BotFather.

Use the command /newbot to create a new bot and get your BOT_TOKEN.

For CHAT_ID - Open Telegram and search for your bot using its username (the one you created with BotFather).
Start a chat with your bot by sending any message (e.g., "Hello").

Then visit - https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

Look for the chat object in the JSON response. Your CHAT_ID will be listed there, typically as chat.id.

Run the script, below, the stuff you give to it will be sent to telegram chat. WTFFF!!!!

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

chmod +x /home/arvypi/GIT/katinelis/fetches/raspberry_humidity.py
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
    file_path = os.path.join(base_dir, "data/cvbankas_ads.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    return {"error": "Data not found"}
```

### Schedule that script to run periodically (and periodically save the data to the file)

Update cronjob file or create a system service to run the script periodically.