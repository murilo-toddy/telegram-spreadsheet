from telegram.ext import Updater
from dotenv import load_dotenv
import os, commands.handler as handler

if os.path.isfile("./.env"): 
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

else:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    
bot = Updater(TELEGRAM_TOKEN)
dsp = bot.dispatcher

handler.register_commands(dsp)