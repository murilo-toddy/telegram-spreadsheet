from spreadsheet import ss
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from utils import subsystems

def log_command(cmd: str): print(f"[!!] Command {cmd} called")

def register_commands(dsp):
    dsp.add_handler(CommandHandler("sw", sw))

def get_listtasks_text(subsystem: str) -> str:
    todo_tasks = "\n".join([f"{index+1} - {row[0]}" 
                            for index, row in enumerate(
                                row for row in ss.sheet(subsystem).get_all_values()
                                if row[1] != "Finalizado" and row[0])])
    
    return (f"<b>Subsistema: {subsystems[subsystem]['name']}</b>\n\n"
                "<u>Tarefas:</u>\n"
                f"{todo_tasks}\n\n"
                "Para concluir uma tarefa, utilize <code>/sw &lt;número | nome da tarefa&gt;</code>"
                ).format(todo_tasks=todo_tasks)



def sw(update: Update, ctx: CallbackContext) -> None:
    task = " ".join(ctx.args)
    print(task)
    log_command("software")
    
    update.message.reply_text(get_listtasks_text("sw"), parse_mode=ParseMode.HTML)