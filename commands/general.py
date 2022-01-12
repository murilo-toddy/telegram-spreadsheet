from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from spreadsheet import SHEET_URL

def send_sheet(update: Update, ctx: CallbackContext):
    update.message.reply_text(f'<a href="{SHEET_URL}">Planilha de Planejamento</a>',
                              parse_mode=ParseMode.HTML)