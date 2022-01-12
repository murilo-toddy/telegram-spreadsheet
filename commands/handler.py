from telegram.ext import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
import commands.subsystems as subsystems
import commands.general as general

def log_command(cmd: str): print(f"[!!] Command {cmd} called")

def register_commands(dsp):
    dsp.add_handler(CommandHandler("bt", subsystems.bt))
    dsp.add_handler(CommandHandler("pt", subsystems.pt))
    dsp.add_handler(CommandHandler("hw", subsystems.hw))
    dsp.add_handler(CommandHandler("sw", subsystems.sw))
    
    dsp.add_handler(CallbackQueryHandler(subsystems.query_handler))
    
    dsp.add_handler(CommandHandler("planilha", general.send_sheet))
