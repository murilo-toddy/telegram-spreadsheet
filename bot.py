from telegram.ext import Updater

import commands.handler as handler
from config import TELEGRAM_TOKEN

# Creates bot instance
bot = Updater(TELEGRAM_TOKEN)
dsp = bot.dispatcher

# Load commands and handlers
handler.register_commands(dsp)
