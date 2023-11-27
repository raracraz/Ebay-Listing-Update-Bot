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

def get_updated_listings(sellers, last_checked):
    all_items = []
    for seller_name in sellers:
        try:
            api = Finding(appid=appid, config_file=None)
            response = api.execute('findItemsAdvanced', {
                'itemFilter': [
                    {'name': 'Seller', 'value': seller_name},
                    {'name': 'StartTimeFrom', 'value': last_checked.strftime('%Y-%m-%dT%H:%M:%S')}
                ]
            })
            response_dict = response.dict()
            if response_dict.get('searchResult', {}).get('_count', '0') != '0':
                items = response_dict['searchResult']['item']
                all_items.extend(items)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
    return all_items

def main():
    sellers = config.get('EbayFilters', 'sellers').split(',')
    # Initialize last_checked to one day before the current time, rounded down to the nearest second
    gmt = pytz.timezone('GMT')
    last_checked = datetime.now(gmt).replace(microsecond=0) - timedelta(days=1)

    updater = Updater(token, use_context=True)

    while True:
        updated_listings = get_updated_listings(sellers, last_checked)
        # Round down current_time to the nearest second
        current_time = datetime.now(gmt).replace(microsecond=0)

        if updated_listings:
            print(f"Found {len(updated_listings)} new listings.")
            for item in updated_listings:
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

        print(f"Updating last_checked to {current_time}")
        last_checked = current_time
        time.sleep(60)  # Wait for 1 minute before checking again

if __name__ == '__main__':
    main()

