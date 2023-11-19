import configparser
import re
import time
import os
import logging
from telethon import TelegramClient, events, sync
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('config.ini')

token = config.get('BotConfig', 'token')

def run_bot():
    try:
        updater = Updater(token, use_context=True)
        
    except Exception as e:
        print(f"Unexpected error: {e}. Retrying in 10 seconds...")
        time.sleep(10)
        run_bot()