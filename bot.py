from telegram.ext import Updater
from config import TELEGRAM_TOKEN
import commands.handler as handler
    
bot = Updater(TELEGRAM_TOKEN)
dsp = bot.dispatcher

handler.register_commands(dsp)