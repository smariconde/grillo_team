
"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import googlesheets, scraper, telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from symbol import Symbol
from config import TELEGRAM_TOKEN


# Enable logging
logging.basicConfig(filename="boty.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hola! El bot está operativo.\n\nEste bot devuelve información financiera de un ticker que se le pase por mensaje.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
'''Ecribir un Ticker y el bot devolverá:

- Gráfico anual con indicadores como EMA 20, SMA 50, SMA 200, Volumen y MACD.
- Datos básicos sobre el precio y el volumen.

Se puede consultar el precio del dólar mediante /dolar
'''
        )


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("➰ Working on it... puede tardar unos segundos")
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    symbol = update.message.text.upper()
    ticker = Symbol(symbol)
    grafico = ticker.chart()
    if grafico is False:
        update.message.reply_text("⚠️ - No es un símbolo válido -")
    else:
        caption = ticker.quote()
        bot.send_photo(chat_id=update.message.chat_id, photo=open('chart.png', 'rb'), caption= caption)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def info(update, context):
    """Responde el porcentaje del rendimiento"""
    update.message.reply_text("➰ Working on it... puede tardar unos segundos")
    update.message.reply_text(googlesheets.info())


def plan(update, context):
    update.message.reply_text("➰ Working on it... puede tardar unos segundos")
    update.message.reply_text(googlesheets.plan())


def performance(update, context):
    update.message.reply_text("➰ Working on it... puede tardar unos segundos")
    update.message.reply_text(googlesheets.performance()) 


def dolar(update, context):
    update.message.reply_text("➰ Working on it... puede tardar unos segundos")
    update.message.reply_text(scraper.dolar())    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("plan", plan))
    dp.add_handler(CommandHandler("performance", performance))
    dp.add_handler(CommandHandler("dolar", dolar))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    #dp.add_handler(MessageHandler(Filters.regex('^([Ii]nfo|[Tt]rades)$'), info))

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
