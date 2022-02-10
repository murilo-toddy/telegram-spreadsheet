from gspread import Worksheet
from telegram import Update
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)

from utils import available_systems, electric_subsystems, mechanics_subsystem
from .generic import (
    timeout,
    cancel,
    get_default_system_message,
    get_conversation,
    load_conversation,
    keyboards,
    load_system_info,
    load_subsystem_info
)
from ..general import log_command, reply_text

# States of conversation
SYSTEM, SUBSYSTEM, TASK, DIFFICULTY, DURATION, COMMENTS = range(6)


# Main function in task concluding command
def conclude_task(update: Update, ctx: CallbackContext) -> int:
    # Initiates new conversation
    load_conversation(update)
    log_command("conclude task")

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
    task_name, desc = "Concluir tarefa", "Modifica o status da tarefa para Concluído na planilha do sistema"
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
    system = get_conversation(update).system
    selected_subsystem = update.message.text
    available_subsystems = electric_subsystems.keys() if system == "ele" else mechanics_subsystem.keys()
    if selected_subsystem not in available_subsystems:
        reply_text(update, "Subsistema não encontrado\nTente novamente")
        return SUBSYSTEM

    load_subsystem_info(update, selected_subsystem)
    return TASK


def difficulty_selector(update: Update, ctx: CallbackContext) -> int:
    conversation = get_conversation(update)
    try:
        task_number = int(update.message.text)
        # Gets text containing all tasks and finds specified task by number
        task_row = [row for row in conversation.tasks.split("\n") if row.startswith(f"{task_number}")][0]
        # Removes number in front
        task_name = task_row.partition(" - ")[2]
        if task_name == "":
            # Task not found in tasks list
            reply_text(update, "O número fornecido não está relacionado com uma tarefa válida\nTente novamente")
            return TASK

    except ValueError:
        # Task not found in tasks list
        reply_text(update, "O número fornecido não está relacionado com uma tarefa válida\nTente novamente")
        return TASK

    ss: Worksheet = conversation.ss.sheet(conversation.subsystem)
    data = ss.get_all_values()
    # Finds corresponding row in spreadsheet
    for index, row in enumerate(data):
        if row[1] == task_name:
            break

    conversation.row = row
    conversation.index = index
    text_message = f"A dificuldade esperada para {row[1]} era de {row[5]}\nForneça a dificuldade real encontrada (0-10)"
    reply_text(update, text_message)

    return DIFFICULTY


def read_comment(update: Update, ctx: CallbackContext) -> int:
    conversation = get_conversation(update)
    try:
        conversation.difficulty = float(update.message.text)
        if conversation.difficulty > 10 or conversation.difficulty < 0:
            # Value out of range
            reply_text(update, "O valor fornecido é inválido\nTente novamente")
            return DIFFICULTY

    except ValueError:
        # Argument is NAN
        reply_text(update, "O valor fornecido é inválido\nTente novamente")
        return DIFFICULTY

    reply_text(update, "Descreva brevemente o porquê desta dificuldade")
    return COMMENTS


def info_confirmation(update: Update, ctx: CallbackContext) -> int:
    conversation = get_conversation(update)
    conversation.comments = update.message.text

    # Updates information in google sheets
    conversation.ss.conclude_task(conversation)

    update.message.reply_text(f"Tarefa {conversation.row[1]} concluída com sucesso!")
    return ConversationHandler.END


# Conversation handler to update between states
conclude_handler = ConversationHandler(
    entry_points=[CommandHandler("end", conclude_task)],
    states={
        SYSTEM: [MessageHandler(Filters.text & ~Filters.command, subsystem_selector)],
        SUBSYSTEM: [MessageHandler(Filters.text & ~Filters.command, task_selector)],
        TASK: [MessageHandler(Filters.text & ~Filters.command, difficulty_selector)],
        DIFFICULTY: [MessageHandler(Filters.text & ~Filters.command, read_comment)],
        COMMENTS: [MessageHandler(Filters.text & ~Filters.command, info_confirmation)],
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=40,
)
