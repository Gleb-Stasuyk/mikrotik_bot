import paramiko
import logging
import os

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
BOTNAME = os.getenv('BOTNAME')
PASSWORD = os.getenv('PASSWORD')

logger = logging.getLogger(__name__)
bot = Bot(token=TELEGRAM_TOKEN)


def ssh_comand(method, address, list_name):
    command = f"ip firewall address-list {method} address={address} list={list_name}"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, PORT, BOTNAME, PASSWORD)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    return lines


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Че ннада?')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Тебе уже не помочь')


def say_hi(update: Update, context: CallbackContext):
    try:
        method, address, list_name = update.message.text.split()
        if method == 'add':
            lines = ssh_comand(method, address, list_name)
            if lines != []:
                update.message.reply_text(f'Ошибка: {lines}')
            else:
                update.message.reply_text('Добавил адрес')
        else:
            update.message.reply_text('Неизвестный метод')

        if method == 'remove':
            pass
    except:
        update.message.reply_text('Ерунду написал')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    #    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, say_hi))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
