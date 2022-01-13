from telegram.ext import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
import commands.subsystems.generic as generic
import commands.general as general

def log_command(cmd: str): print(f"[!!] Command {cmd} called")

def register_commands(dsp):
    dsp.add_handler(CommandHandler("bt", generic.bt))
    dsp.add_handler(CommandHandler("pt", generic.pt))
    dsp.add_handler(CommandHandler("hw", generic.hw))
    dsp.add_handler(CommandHandler("sw", generic.sw))
    
    dsp.add_handler(CallbackQueryHandler(generic.query_handler))
    dsp.add_handler(CallbackQueryHandler(general.send_sheet))
    
    dsp.add_handler(CommandHandler("planilha", general.send_sheet))
