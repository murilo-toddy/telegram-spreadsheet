from telegram.ext import CommandHandler, CallbackQueryHandler
import commands.subsystems.task_register as task_register
import commands.subsystems.generic as generic
import commands.general as general
from spreadsheet import commands

def log_command(cmd: str): print(f"[!!] Command {cmd} called")

def register_commands(dsp):
    dsp.add_handler(CommandHandler("bt", generic.bt))
    dsp.add_handler(CommandHandler("pt", generic.pt))
    dsp.add_handler(CommandHandler("hw", generic.hw))
    dsp.add_handler(CommandHandler("sw", generic.sw))
    
    dsp.add_handler(CallbackQueryHandler(generic.query_handler))
    dsp.add_handler(CallbackQueryHandler(general.send_sheet))
    
    dsp.add_handler(CommandHandler("planilha", general.send_sheet))

    dsp.add_handler(task_register.register_handler)

    for cmd in commands.sheet("cmd").get_all_values()[1:]:
        dsp.add_handler(CommandHandler(command=cmd[0], callback=general.spreadsheet_return_text))
