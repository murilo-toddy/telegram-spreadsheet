from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)

from spreadsheet import systems
from .generic import (
    get_default_system_message,
    timeout,
    cancel,
    load_conversation,
    get_conversation,
    get_task_lister_text,
)
from ..general import log_command, reply_text
from .generic import load_system_info, load_subsystem_info, keyboards
from utils import available_systems, electric_subsystems, mechanics_subsystem

# States of conversation
SYSTEM, SUBSYSTEM, TASK = range(3)


# Home function
# TODO Enable subsystem arguments for faster starting
def start_task(update: Update, ctx: CallbackContext) -> int:
    # Initiates new conversation
    load_conversation(update)
    log_command("start task")

    if ctx.args:
        arg = ctx.args[0].strip().lower()
        if arg in available_systems:
            # System selected
            load_system_info(update, selected_system=arg)
            return SUBSYSTEM

        elif arg in electric_subsystems.keys():
            # Electric subsystem selected
            load_system_info(update, selected_system="ele")
            load_subsystem_info(update, selected_subsystem=arg)
            return TASK

        elif arg in mechanics_subsystem.keys():
            # Mechanics subsystem selected
            load_system_info(update, selected_system="mec")
            load_subsystem_info(update, selected_subsystem=arg)
            return TASK

    # No/invalid arguments passed, prompts for system
    task_name, desc = "Iniciar tarefa", "Modifica o status da tarefa para Fazendo na planilha do sistema"
    reply_text(update, get_default_system_message(task_name, desc), keyboards["system"])
    return SYSTEM


def subsystem_selector(update: Update, ctx: CallbackContext) -> int:
    selected_system = update.message.text
    if selected_system not in available_systems:
        reply_text(update, "Sistema não encontrado\nTente novamente")
        return SYSTEM

    load_system_info(update, selected_system)
    return SUBSYSTEM


def task_selector(update: Update, ctx: CallbackContext) -> int:
    selected_system = get_conversation(update).system
    selected_subsystem = update.message.text
    available_subsystems = electric_subsystems.keys() if selected_system == "ele" else mechanics_subsystem.keys()
    if selected_subsystem not in available_subsystems:
        reply_text(update, "Subsistema não encontrado\nTente novamente")
        return SUBSYSTEM

    load_subsystem_info(update, selected_subsystem)
    return TASK


def task_starter(update: Update, ctx: CallbackContext) -> int:
    try:
        # Verifies task is valid
        conversation = get_conversation(update)
        task = int(update.message.text)
        task_row = [row for row in conversation.tasks.split("\n") if row.startswith(f"{task}")][0]
        task_name = task_row.split(" - ")[1]
        conversation.task = task_name
    except:
        # Task is invalid
        update.message.reply_text("Forneça um número válido")
        return TASK

    # Finds task index in spreadsheet
    conversation.ss.start_task(conversation)
    update.message.reply_text(f"Tarefa {task_name} iniciada com sucesso!")
    return ConversationHandler.END


# Conversation handler to update between states
start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_task)],
    states={
        SYSTEM: [MessageHandler(Filters.text & ~Filters.command, subsystem_selector)],
        SUBSYSTEM: [MessageHandler(Filters.text & ~Filters.command, task_selector)],
        TASK: [MessageHandler(Filters.text & ~Filters.command, task_starter)],
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=30,
)
