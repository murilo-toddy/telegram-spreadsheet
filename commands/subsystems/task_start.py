from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from gspread import Worksheet
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)
from commands.subsystems.generic import get_default_system_message, timeout, cancel
from commands.subsystems.task_list import get_task_lister_text
from spreadsheet import systems
from commands.general import log_command

# States of conversation
SYSTEM, SUBSYSTEM, TASK = range(3)

# Dictionary containing all needed information about the task
task_start = {"ss": None, "dict": None, "system": "", "subsystem": "", "tasks": ""}


# Home function
# TODO Enable subsystem arguments for faster starting
def start_task(update: Update, ctx: CallbackContext) -> int:
    log_command("start")
    if not ctx.args:
        system = [["ele", "mec"]]
        update.message.reply_text(
            get_default_system_message("Iniciar tarefa", ""),
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(system),
        )
        return SYSTEM


# TODO Find a way to extract common conversation methods
# System selecting method
def system(update: Update, ctx: CallbackContext) -> int:
    system = update.message.text
    if system == "ele":
        subsystem_selector = [["bt", "pt"], ["hw", "sw"]]
    elif system == "mec":
        subsystem_selector = [["ch"]]
    else:
        update.message.reply_text("Sistema não encontrado", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    # Saves pertinent information in global variable
    global task_start
    task_start["system"] = system
    task_start["dict"] = systems["ele"]["sub"] if system == "ele" else systems["mec"]["sub"]
    task_start["ss"] = systems["ele"]["ss"] if system == "ele" else systems["mec"]["ss"]

    update.message.reply_text(
        "Informe o subsistema",
        reply_markup=ReplyKeyboardMarkup(subsystem_selector, one_time_keyboard=True),
        parse_mode=ParseMode.HTML,
    )
    return SUBSYSTEM


# Subsystem selecting method
def subsystem(update: Update, ctx: CallbackContext) -> int:
    subsystem = update.message.text
    global task_start
    task_start["subsystem"] = subsystem
    task_start["tasks"] = get_task_lister_text(task_start["system"], task_start["subsystem"])
    reply_text = (
        f"<b>Subsistema: {task_start['dict'][subsystem]['name']}</b>\n\n"
        f"{task_start['tasks']}\n\n"
        "Selecione da lista acima o número da tarefa que deseja iniciar"
    )
    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    return TASK


def task(update: Update, ctx: CallbackContext):
    try:
        # Verifies task is valid
        global task_start
        task = int(update.message.text)
        task_row = [row for row in task_start["tasks"].split("\n") if row.startswith(f"{task}")][0]
        task_name = task_row.split(" - ")[1]
    except:
        # Task is invalid
        update.message.reply_text("Forneça um número válido")
        return TASK

    # Finds task index in spreadsheet
    ss: Worksheet = task_start["ss"].sheet(task_start["subsystem"])
    data = ss.get_all_values()
    for index, row in enumerate(data):
        if row[1] == task_name:
            break

    # Updates status and returns
    ss.update_acell(f"C{index+1}", "Fazendo")
    update.message.reply_text(f"Tarefa {task_name} iniciada com sucesso!")
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_task)],
    states={
        SYSTEM: [MessageHandler(Filters.text & ~(Filters.command), system)],
        SUBSYSTEM: [MessageHandler(Filters.text & ~(Filters.command), subsystem)],
        TASK: [MessageHandler(Filters.text & ~(Filters.command), task)],
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=30,
)
