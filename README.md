# Ebay Listing Update Bot
This is a bot that monitors eBay seller listings and sends notifications to your Telegram account when there are updates.

## Workflow Diagram
![Blank diagram](https://github.com/raracraz/Ebay-Listing-Update-Bot/assets/88528326/98c7e235-a9b6-44d9-8dda-ef6fafbd9f0a)

## Features
- [x] Monitor eBay seller listings
- [x] Send notifications to Telegram account/group

## Usage
1. Clone this repository
2. Install dependencies
```py -m pip install -r requirements.txt```
3. Create a Telegram bot and get the bot token
4. Create a Telegram group and add the bot to the group
5. Get the group chat id
6. Register a developer account on eBay and get the app id
7. Create a Config.ini file in the root directory of the repository and fill in the details
```
[TelegramBotConfig]
token = YOUR_BOT_TOKEN
my_user_id = YOUR_USER_ID
dest_channel_id = YOUR_GROUP_CHAT_ID

[EbayConfig]
appid = YOUR_EBAY_APP_ID

[EbayFilters]
seller_name = SELLER_NAME (in URL of seller's page)
```
