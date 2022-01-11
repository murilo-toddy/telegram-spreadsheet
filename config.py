from spreadsheet import Spreadsheet
from dotenv import load_dotenv
import os, telebot

SHEET_AUTH_FILE = 'client_secret.json'
SHEET_NAME = "Planejamento Manufatura T-06 Prime"
SHEET_SCOPE = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]

debug = True
subsystems = {
    "bt": 1546038790,
    "pt": 1047261973,
    "hw": 0,
    "sw": 447316715
}

ss = Spreadsheet(SHEET_NAME, SHEET_SCOPE, SHEET_AUTH_FILE, debug)
for subsystem, sheet_id in subsystems.items(): 
    ss.add_sheet(subsystem, sheet_id)

if os.path.isfile("./.env"): 
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

else:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    
bot = telebot.TeleBot(TELEGRAM_TOKEN)
