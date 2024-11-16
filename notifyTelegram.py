import logging
import requests
import re
from datetime import datetime
import configparser
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Helper Function:
async def get_hisse(name='BAYRK', exchange='IST'):
    url = f'https://www.google.com/finance/quote/{name.upper()}:{exchange.upper()}'
    response = requests.get(url)
    data_exchange = re.search(r'data-exchange="?([0-9\.A-Z]*)"?', response.text).group(1)
    data_currency_code = re.search(r'data-currency-code="?([0-9\.A-Z]*)"?', response.text).group(1)
    data_last_price = re.search(r'data-last-price="?([0-9\.A-Z]*)"?', response.text).group(1)
    data_last_normal_market_timestamp = int(re.search(r'data-last-normal-market-timestamp="?([0-9\.A-Z]*)"?', response.text).group(1))
    data_tz_offset = re.search(r'data-tz-offset="?([0-9\.A-Z]*)"?', response.text).group(1)
    return f'BAYRK => exchange: {data_exchange} last price:{data_last_price} {data_currency_code} last normal market time: {datetime.fromtimestamp(data_last_normal_market_timestamp)}'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def hisse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hisse = await get_hisse()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=hisse)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.conf')
    bot_token = config['DEFAULT']['BOT_TOKEN']
    application = ApplicationBuilder().token(bot_token).build()
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    hisse_handler = CommandHandler('hisse', hisse)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(hisse_handler)

    application.run_polling()