"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Hello! I'm waiting for your orders.")


def help(update, context):
    update.message.reply_text('Command list:\n/air - get information about air')


def get_intent(update, context):
    data = {"text": update.message.text}
    r = requests.post(url='http://127.0.0.1:5000/get-intent', json=data)
    update.message.reply_text(r.json()['response'])


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def air_info(update, context):
    update.message.reply_text('The air info follows...')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("998116369:AAGrvjdugSsYOklXcQ4yZxWWpyisLiAZtVE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('air', air_info))

    # on noncommand i.e message - get intent of the message
    dp.add_handler(MessageHandler(Filters.text, get_intent))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
