import os
from dotenv import load_dotenv

if os.path.isfile("./.env"): 
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    COMMANDS_SHEET_ID = os.getenv("COMMANDS_SHEET_ID")
    ELE_SHEET_ID = os.getenv("ELE_SHEET_ID")

else:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    COMMANDS_SHEET_ID = os.environ["COMMANDS_SHEET_ID"]
    ELE_SHEET_ID = os.environ["ELE_SHEET_ID"]
    