from spreadsheet import Spreadsheet
from telegram.ext import Updater
from dotenv import load_dotenv
import os, commands

if os.path.isfile("./.env"): 
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

else:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    
bot = Updater(TELEGRAM_TOKEN)
dsp = bot.dispatcher

commands.register_commands(dsp)