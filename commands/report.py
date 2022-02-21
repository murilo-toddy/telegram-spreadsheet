from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from config import REPORT_CHAT_ID
from .general import send_message, send_message_to


# Command that enables users to report malfunctions
def report_command(update: Update, ctx: CallbackContext):
    send_message(update, ctx, "Report enviado!")
    send_message_to(ctx, REPORT_CHAT_ID, "reportado")
