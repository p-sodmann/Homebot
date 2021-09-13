from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, CallbackContext
from telegram import ParseMode, Bot
from telegram import Update
from api_token import token
import schedule

import logging

from site_parser.ebay import EbayParser
from site_parser.immowelt import ImmoweltParser

# set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(
    token=token, 
    use_context=True, 
    request_kwargs={'read_timeout': 6, 'connect_timeout': 7}
)

dispatcher = updater.dispatcher

import bot_messages

def start(update, context):
    global users

    chat_id = update.message.chat_id
    
    context.user_data["already_seen"] = []
    context.user_data["chat_id"] = chat_id
    
    context.bot.send_message(chat_id=chat_id, text=bot_messages.welcome_message)

    context.job_queue.run_repeating(scrape, interval=60*10, first=5, context=context)

def scrape(callback: CallbackContext):
    print(f"scraping for {callback.job.context.user_data['chat_ id']}")

    new_immos = []
    for parser in parsers:
        new_immos += parser(callback)

    
    for immo in new_immos[:5]:
        callback.bot.sendPhoto(
            chat_id=callback.job.context.user_data["chat_id"],
            photo = immo.image_link,
            caption=str(immo),
            parse_mode=ParseMode.HTML
        )
        

if __name__ == "__main__":
    users = []
    ctx = None
    parsers = [
        EbayParser("97070", 1_000_000, 10),
        ImmoweltParser("wuerzburg", 1_000_000, 10)
    ]

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()

    # let it allow to close gracefully
    updater.idle()