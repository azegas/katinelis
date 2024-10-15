'''
What the hell. Integration with telegram.

Go to Telegram and search for the BotFather.

Use the command /newbot to create a new bot and get your BOT_TOKEN.

For CHAT_ID - Open Telegram and search for your bot using its username (the one you created with BotFather).
Start a chat with your bot by sending any message (e.g., "Hello").

Then visit - https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

Look for the chat object in the JSON response. Your CHAT_ID will be listed there, typically as chat.id.

Run the script, below, the stuff you give to it will be sent to telegram chat. WTFFF!!!!

'''

import json
import requests
import os

BOT_TOKEN = '7982144540:AAHVKMg0vf_AeDrXDOK84UFHg5jmUmU1qHE'
CHAT_ID = '6931316670' # mano personal chat su botu
# CHAT_ID = '-4507158114' # mm2 grupe
data_folder = '../data'


def main():
    filename = 'random_quote.json'
    with open(os.path.join(data_folder, filename)) as f:
        data = json.load(f)
        send_message(json.dumps(data))  # Send JSON data as a string

def send_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)


if __name__ == "__main__":
    main()