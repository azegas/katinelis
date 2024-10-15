# mms == Magic mirror 2

## Install rasberry OS

Use `Raspberry pi imager` bla.

For options:

```bash
sudo raspi-config
```

## Vertical monitor mode

I wish there was `screen layout editor` GUI in raspi settings display section present by default ([like here](https://www.makeuseof.com/how-to-rotate-your-raspberry-pi-screen-without-moving-the-display)), but it's not, so have to do it over the terminal.

```bash
# check what my display is named (HDMI-0 or HDMI-1) 
xrandr
# rotate the display (no reboot needed)
xrandr --output HDMI-1 --rotate left
```


Lasting GUI way:

To install the "Screen Configuration" tool (known as arandr or the Raspberry Pi "Screen Layout Editor") on your Raspberry Pi, follow these steps:

```bash
sudo apt install arandr
```

Tuomet preferences -> screen configuration -> layout -> bla ir nusistatyk kaip reikia.


## If GUI is not working anymore

Default GUI - `pixel desktop`.

```bash
sudo apt update
sudo apt upgrade
sudo apt install --reinstall raspberrypi-ui-mods
sudo raspi-config

# Go to System Options.
# Select Boot/Auto Login.
# Choose Desktop GUI, automatically logged in or Desktop GUI, 
# requiring login based on your preference.

# reboot pi
```

## About all the services

## About cronjobs

## Start chromium automatically by default

`start_chromium.sh` file.


# Things TODO

- [x] max 9 jobs gali buti atvaizduojami
- [ ] write to file how the temperature went during the night. Take reading at 5 different points in time maybe? separate cronjob? Then display them during in the magic mirror.
- [x] write date when job was posted
- [x] filter by job company
- [ ] wind information
- [ ] spanish word of the day
- [x] paziurek ideju is lifeapi
- [x] pridek rescuetime data
- [x] koks oras madride
- [x] pamegink linkedina del job searches
- [x] pamegink google calendar embed i website (jokiu fetchu hopefully...) - possible, did it, but not actually needed for us
- [ ] arba google trends explore trends - https://trends.google.com/trends/explore?hl=en-GB
- [ ] google trends paskutiniu 24val LT - https://trends.google.com/trending?geo=LT&hl=en-GB&hours=24
- [ ] google trends united states 4 hour - https://trends.google.com/trending?geo=US&hl=en-GB&hours=4
- [x] alphavantage - tik 25 queires KRC - https://www.alphavantage.co/documentation/
- [x] stocks - most advanced most declined
- [x] stocks - top gainers
- [x] stocks - top losers
- [x] trading view stock charts from (unfortunately lags a lot) https://www.tradingview.com/widget-docs/widgets/symbol-details/
- [x] stocks - volume
- [x] quote of the day
- [ ] google trends topics - https://trends.google.com/trending?geo=US
- [ ] notification when big change happened or smth like that. or simply show todays trends in telegram kaip zinute
- [x] raspberry pi uptime 
- [x] Running eilutė kaip NASDAQe (labai trukineja ji raspberryje)
- [ ] fondu duomenys - https://www.swedbank.lt/private/investor/funds/allFunds/list/details
- [x] humidity inside
- [x] temperature in
- [x] temperature out
- [ ] humidity UI sitaip SEK TIK 24h - https://i0.wp.com/blog.balena.io/wp-content/uploads/2021/07/sensev2.png?fit=1200%2C628&ssl=1
- [x] log file for when was fetched and if successs or not (aisku matai in flask terminal, but anyway)
- [ ] switch one the display kai kas nors priarteja - https://tutorials-raspberrypi.com/connect-and-control-raspberry-pi-motion-detector-pir/, https://www.youtube.com/watch?v=Tw0mG4YtsZk
- [X] fix period for charts!!! make it dynamic
- [x] covid cases (not so needed and kinda hard to fetch)
- [x] population (not so needed and kinda hard to fetch)
- [x] indication, that the page has refreshed


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

### Then we need to create a socket that the client can call:

```python
@socketio.on('request_from_client_to_server_for_cvbankas_data') # this is the socket that the client will call
def handle_cvbankas_update_request():
    # 'emit' is a Socket.IO method used to send events from the server to the client
    # An alternative could be 'send', but 'emit' is more flexible as it allows custom event names
    # Here, it sends the 'response_from_server_to_client_with_cvbankas_data' event with the data from read_cvbankas_data()
    emit('response_from_server_to_client_with_cvbankas_data', read_cvbankas_data())
```

### Then we describe how often the client will be calling the socket:
 
```js
setInterval(() => {
    socket.emit('request_from_client_to_server_for_cvbankas_data');
}, 1000);
```

### Describe what will happen when the data is received:

Server emitted `response_from_server_to_client_with_cvbankas_data`, so when the client gets `response_from_server_to_client_with_cvbankas_data` and data with it, it will call `updateCvbankasData(data)` (create this js function) in `domUpdates.js`

Describe how the DOM will be changed with the received data:

```js
export function updateCvbankasData(data) {
    const jobsContainer = document.getElementById('cvbankas_jobs');
    jobsContainer.innerHTML = ''; // Clear previous content
```

Add this to `main.js`, dont forget to import the `updateCvbankasData` function from `domUpdates.js`

```js
socket.on('response_from_server_to_client_with_cvbankas_data', (data) => {
    updateCvbankasData(data);
});
```

### A place where the data will be displayed:

```html
<div id="cvbankas_jobs" class="row"></div>
```

### Schedule that script to run periodically (and periodically save the data to the file)

Update cronjob file or create a system service to run the script periodically.