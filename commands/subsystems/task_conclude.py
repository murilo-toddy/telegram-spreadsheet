from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)
from gspread import Worksheet
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
        arg = ctx.args[0]
        if arg in available_systems:
            # System selected
            load_system_info(update, selected_system=arg)
            return SUBSYSTEM

        elif arg in list(electric_subsystems.keys()):
            # Electric subsystem selected
            load_system_info(update, selected_system="ele")
            load_subsystem_info(update, selected_subsystem=arg)
            return TASK

        elif arg in list(mechanics_subsystem.keys()):
            # Mechanics subsystem selected
            load_system_info(update, selected_system="mec")
            load_subsystem_info(update, selected_subsystem=arg)
            return TASK

    else:
        # No/invalid arguments passed, prompts for system
        task, desc = "Concluir tarefa", "Modifica o status da tarefa para Concluído na planilha do sistema"
        reply_text(update, get_default_system_message(task, desc), keyboards["system"])
        return SYSTEM


def subsystem_selector(update: Update, ctx: CallbackContext) -> int:
    selected_system = update.message.text
    if selected_system not in available_systems:
        update.message.reply_text("Sistema não encontrado\nTente novamente", reply_markup=ReplyKeyboardRemove())
        return SYSTEM

    load_system_info(update, selected_system)
    return SUBSYSTEM


def task_selector(update: Update, ctx: CallbackContext) -> int:
    selected_subsystem = update.message.text
    load_subsystem_info(update, selected_subsystem)
    return TASK


def difficulty_selector(update: Update, ctx: CallbackContext) -> int:
    # TODO refactor
    conversation = get_conversation(update)
    try:
        task = int(update.message.text)
        task_row = [row for row in conversation.tasks.split("\n") if row.startswith(f"{task}")][0]
        task_name = task_row.split(" - ")[1]
    except Exception:
        update.message.reply_text("Forneça um número válido")
        return TASK

    ss: Worksheet = conversation.ss.sheet(conversation.subsystem)
    data = ss.get_all_values()
    for index, row in enumerate(data):
        if row[1] == task_name:
            break

    conversation.row = row
    conversation.index = index
    update.message.reply_text(
        f"A dificuldade esperada para {row[1]} era de {row[5]}\nForneça a dificuldade real encontrada (0-10)"
    )

    return DIFFICULTY


def read_comment(update: Update, ctx: CallbackContext) -> int:
    conversation = get_conversation(update)
    conversation.difficulty = update.message.text
    update.message.reply_text("Descreva brevemente o porquê desta dificuldade")
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
