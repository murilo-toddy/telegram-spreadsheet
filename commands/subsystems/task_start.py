from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)
from .generic import get_default_system_message, timeout, cancel, load_conversation, get_conversation
from .task_list import get_task_lister_text
from ..general import log_command
from spreadsheet import systems

# States of conversation
SYSTEM, SUBSYSTEM, TASK = range(3)


# Home function
# TODO Enable subsystem arguments for faster starting
def start_task(update: Update, ctx: CallbackContext) -> int:
    log_command("start")
    load_conversation(update)
    if not ctx.args:
        system = [["ele", "mec"]]
        update.message.reply_text(
            get_default_system_message(
                "Iniciar tarefa",
                "Modifica o status de uma tarefa para Fazendo na planilha de mapeamento do sistema",
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(system),
        )
        return SYSTEM


# TODO Find a way to extract common conversation methods
# System selecting method
def system(update: Update, ctx: CallbackContext) -> int:
    # TODO rename variables
    system = update.message.text
    if system == "ele":
        subsystem_selector = [["bt", "pt"], ["hw", "sw"]]
    elif system == "mec":
        subsystem_selector = [["ch"]]
    else:
        update.message.reply_text("Sistema não encontrado", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    # Saves pertinent information in conversation
    conversation = get_conversation(update)
    conversation.system = system
    conversation.dict = systems[system]["sub"]
    conversation.ss = systems[system]["ss"]

    update.message.reply_text(
        "Informe o subsistema",
        reply_markup=ReplyKeyboardMarkup(subsystem_selector, one_time_keyboard=True),
        parse_mode=ParseMode.HTML,
    )
    return SUBSYSTEM


# Subsystem selecting method
def subsystem(update: Update, ctx: CallbackContext) -> int:
    subsystem = update.message.text

    conversation = get_conversation(update)
    conversation.subsystem = subsystem
    conversation.tasks = get_task_lister_text(conversation.system, conversation.subsystem)

    reply_text = (
        f"<b>Subsistema: {conversation.dict[subsystem]['name']}</b>\n\n"
        f"{conversation.tasks}\n\n"
        "Selecione da lista acima o número da tarefa que deseja iniciar"
    )
    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    return TASK


def task(update: Update, ctx: CallbackContext) -> int:
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
    # TODO create method in electric spreadsheet
    conversation.ss.start_task(conversation)
    update.message.reply_text(f"Tarefa {task_name} iniciada com sucesso!")
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_task)],
    states={
        SYSTEM: [MessageHandler(Filters.text & ~Filters.command, system)],
        SUBSYSTEM: [MessageHandler(Filters.text & ~Filters.command, subsystem)],
        TASK: [MessageHandler(Filters.text & ~Filters.command, task)],
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=30,
)
