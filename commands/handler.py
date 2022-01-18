from telegram.ext import CommandHandler, CallbackQueryHandler
import commands.subsystems.status_updater as status_updater
import commands.subsystems.task_register as task_register
import commands.subsystems.task_list as task_list
import commands.subsystems.generic as generic
import commands.general as general
from spreadsheet import commands

def log_command(cmd: str): print(f" [!!] Command {cmd} called")

def register_commands(dsp):
    dsp.add_handler(CommandHandler("list", task_list.subsystem_task_lister))
    dsp.add_handler(CommandHandler("end",  status_updater.conclude_task))
    dsp.add_handler(CommandHandler("init", status_updater.start_task))
    
    dsp.add_handler(CommandHandler("planilha", general.send_sheet))
    dsp.add_handler(CommandHandler("refresh",  general.update_sheet_commands))
    
    dsp.add_handler(CallbackQueryHandler(generic.query_handler))
    dsp.add_handler(task_register.register_handler)

    for cmd in commands.sheet("cmd").get_all_values()[1:]:
        dsp.add_handler(CommandHandler(command=cmd[0], callback=general.spreadsheet_return_text))

    print("[!] Commands loaded")
