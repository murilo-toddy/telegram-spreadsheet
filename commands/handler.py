from telegram.ext import CommandHandler, CallbackQueryHandler
import commands.subsystems.task_conclude as task_conclude
import commands.subsystems.task_start as task_start
import commands.subsystems.task_register as task_register
import commands.subsystems.task_list as task_list
import commands.subsystems.query_handler as query_handler
import commands.general as general
from spreadsheet import commands
import commands.help as help


# Registers command and callback handlers into bot
def register_commands(dsp) -> None:
    dsp.add_handler(CommandHandler("help", help.help_command))

    dsp.add_handler(CommandHandler("list", task_list.subsystem_task_lister))

    dsp.add_handler(CommandHandler("planilha", general.send_sheet))
    dsp.add_handler(CommandHandler("refresh", general.update_sheet_commands))

    dsp.add_handler(CallbackQueryHandler(query_handler.query_handler))
    dsp.add_handler(task_register.register_handler)
    dsp.add_handler(task_start.start_handler)
    dsp.add_handler(task_conclude.conclude_handler)

    # Loads commands from Commands Spreadsheet
    for cmd in commands.sheet("cmd").get_all_values()[1:]:
        dsp.add_handler(CommandHandler(command=cmd[0], callback=general.spreadsheet_return_text))

    print("\n  [!] Commands loaded")
