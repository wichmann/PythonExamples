#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name:        bot - simple example for a telegram bot
# Usage:       ./bot.py
# Author:      Christian Wichmann
# Created:     13.06.2019
# Copyright:   (c) Christian Wichmann 2019
# Licence:     GNU GPL
#-------------------------------------------------------------------------------

from telegram.ext import Updater, CommandHandler
from telegram import bot

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Token, das vom @BotFather bei Anlegen des Bots ausgegeben wurde
TOKEN = 'TELEGRAM_TOKEN'


def hello(bot, update):
    """Implementiert ein einfaches Kommando, das den sendenden Nutzer mit seinem Vornamen begrüßt."""
    print('Nachricht empfangen...')
    update.message.reply_text('Hallo {}'.format(update.message.from_user.first_name))


def callback_repeating_task(bot, job):
    """Sendet bei jedem Aufruf eine Standardnachricht an eine bestimmte Chat-ID."""
    bot.send_message(chat_id='CHAT ID', text='Eine Nachricht...')


# erzeuge Warteschlage für Aufgaben, die im Hintergrund abgearbeitet werden
updater = Updater(TOKEN)
jobs = updater.job_queue

# füge neuen Handler für den Befehl "hello" hinzu
updater.dispatcher.add_handler(CommandHandler('hello', hello))

# rufe alle 10 Sekunden die Callback-Funktion auf
job_minute = jobs.run_repeating(callback_repeating_task, interval=10, first=0)

# beginne auf neue Nachrichten zu warten
updater.start_polling()
updater.idle()
