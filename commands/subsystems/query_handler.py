import commands.subsystems.task_list as task_list
from telegram.ext import CallbackContext
from telegram import Update


def query_handler(update: Update, ctx: CallbackContext) -> None:
    query = update.callback_query.data
    [cmd, *args] = query.split(" ")

    if cmd == "list":
        task_list.task_lister(update, ctx, args)
