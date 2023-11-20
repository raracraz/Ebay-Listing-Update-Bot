import configparser
from datetime import datetime, timedelta
import time
import pytz 
import json
import logging
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from telethon import TelegramClient, events, sync
import telegram
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Updater


logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

appid = config.get('EbayConfig', 'appid')
token = config.get('TelegramBotConfig', 'token')
my_user_id = int(config.get('TelegramBotConfig', 'my_user_id'))
dest_channel_id = config.get('TelegramBotConfig', 'dest_channel_id')

def get_updated_listings(seller_name, last_checked):
    try:
        appid = config.get('EbayConfig', 'appid')
        api = Finding(appid=appid, config_file=None)
        response = api.execute('findItemsAdvanced', {
            'itemFilter': [
                {'name': 'Seller', 'value': str(seller_name)},
                {'name': 'StartTimeFrom', 'value': last_checked.strftime('%Y-%m-%dT%H:%M:%S')}
            ]
        })
        with open('output.json', 'w') as f:
            json.dump(response.dict(), f, indent=4, sort_keys=True)
        return response.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def main():
    seller_name = config.get('EbayFilters', 'seller_name')
    # Initialize last_checked to one day before the current time
    gmt = pytz.timezone('GMT')
    last_checked = datetime.now(gmt) - timedelta(days=1)

    updater = Updater(token, use_context=True)

    while True:
        updated_listings = get_updated_listings(seller_name, last_checked)

        # Update last_checked to the current time before checking for new listings
        current_time = datetime.now(gmt)

        if updated_listings.get('searchResult', {}).get('_count', '0') != '0':
            items = updated_listings['searchResult']['item']
            print(f"Found {len(items)} new listings.")

            for item in items:
                message = f"New item: {item['title']} at {item['viewItemURL']}"
                try:
                    updater.bot.send_message(chat_id=dest_channel_id, text=message)
                    time.sleep(1)  # Short pause to prevent hitting rate limit
                except telegram.error.RetryAfter as e:
                    print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds.")
                    time.sleep(e.retry_after)
                    updater.bot.send_message(chat_id=dest_channel_id, text=message)
        else:
            print("No new listings found.")

        # Update last_checked to the time before the listings check
        last_checked = current_time
        time.sleep(60)  # Wait for 1 minutes before checking again

if __name__ == '__main__':
    main()

