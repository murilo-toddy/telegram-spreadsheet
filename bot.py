from telegram.ext import Updater

from config import *
import commands.handler as handler

# Creates bot instance
bot = Updater(TELEGRAM_TOKEN)
dsp = bot.dispatcher

# Load commands and handlers
handler.register_commands(dsp)
