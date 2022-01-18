from telegram.ext import Updater
from config import TELEGRAM_TOKEN
import commands.handler as handler

# Creates bot instance
bot = Updater(TELEGRAM_TOKEN)
dsp = bot.dispatcher

# Loads commands and handlers
handler.register_commands(dsp)
