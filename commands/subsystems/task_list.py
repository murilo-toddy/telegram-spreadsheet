from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils import subsystems
from spreadsheet import ss


def get_task_lister_text(subsystem: str) -> str:
    todo_tasks = "\n".join([f"{index+1} - {row[1]}" 
                            for index, row in enumerate(
                                row for row in ss.sheet(subsystem).get_all_values()[1:]
                                if row[2] != "Concluído" and row[1])])
    
    return (f"<b>Subsistema: {subsystems[subsystem]['name']}</b>\n\n"
                "<u>Tarefas:</u>\n"
                f"{todo_tasks}"
                ).format(todo_tasks=todo_tasks)


def subsystem_task_lister(update: Update, ctx: CallbackContext, sub: str, args: str) -> None:
    if not args:
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=get_task_lister_text(sub), parse_mode=ParseMode.HTML)

    else:
        print(f"Conclude task {args}")
        