from commands.subsystems.generic import get_default_system_message
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)
from spreadsheet import electric_ss, mechanics_ss
from utils import ele_subsystems, mec_subsystems
from commands.subsystems.generic import timeout, cancel
from commands.subsystems.task_list import get_task_lister_text
from gspread import Worksheet
from commands.general import log_command

# States of conversation
SYSTEM, SUBSYSTEM, TASK, DIFFICULTY, DURATION, COMMENTS = range(6)

# Conclude task info
end_task = {
    "ss": None,
    "dict": None,
    "system": "",
    "subsystem": "",
    "tasks": "",
    "row": "",
    "index": "",
    "difficulty": "",
    "comments": "",
}

# Dictionary of tasks in progress
conversation_task_info = {}


def conclude_task(update: Update, ctx: CallbackContext) -> int:
    log_command("conclude")
    if not ctx.args:
        system = [["ele", "mec"]]
        update.message.reply_text(
            get_default_system_message("Concluir tarefa"),
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(system),
        )
        return SYSTEM


def system(update: Update, ctx: CallbackContext) -> int:
    system = update.message.text
    if system == "ele":
        subsystem_selector = [["bt", "pt"], ["hw", "sw"]]
    elif system == "mec":
        subsystem_selector = [["ch"]]
    else:
        update.message.reply_text("Sistema não encontrado", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    global end_task
    end_task["system"] = system
    end_task["dict"] = ele_subsystems if system == "ele" else mec_subsystems
    end_task["ss"] = electric_ss if system == "ele" else mechanics_ss

    update.message.reply_text(
        "Informe o subsistema",
        reply_markup=ReplyKeyboardMarkup(subsystem_selector, one_time_keyboard=True),
        parse_mode=ParseMode.HTML,
    )
    return SUBSYSTEM


def subsystem(update: Update, ctx: CallbackContext) -> int:
    subsystem = update.message.text
    global end_task
    end_task["subsystem"] = subsystem
    end_task["tasks"] = get_task_lister_text(end_task["system"], end_task["subsystem"])
    reply_text = (
        f"<b>Subsistema: {end_task['dict'][subsystem]['name']}</b>\n\n"
        f"{end_task['tasks']}\n\n"
        "Selecione da lista acima o número da tarefa que deseja concluir"
    )
    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    return TASK


def task(update: Update, ctx: CallbackContext):
    try:
        global end_task
        task = int(update.message.text)
        task_row = [row for row in end_task["tasks"].split("\n") if row.startswith(f"{task}")][0]
        task_name = task_row.split(" - ")[1]
    except:
        update.message.reply_text("Forneça um número válido")
        return TASK

    ss: Worksheet = end_task["ss"].sheet(end_task["subsystem"])
    data = ss.get_all_values()
    for index, row in enumerate(data):
        if row[1] == task_name:
            break

    end_task["row"] = row
    end_task["index"] = index
    update.message.reply_text(
        f"A dificuldade esperada para esta tarefa era de {row[5]}\nForneça a dificuldade real encontrada (0-10)"
    )

    return DIFFICULTY


def difficulty(update: Update, ctx: CallbackContext):
    global end_task
    end_task["difficulty"] = update.message.text
    update.message.reply_text("Descreva brevemente o porquê desta dificuldade")
    return COMMENTS


def comments(update: Update, ctx: CallbackContext):
    global end_task
    end_task["comments"] = update.message.text

    index = end_task["index"] + 1
    ss: Worksheet = end_task["ss"].sheet(end_task["subsystem"])

    ss.update_acell(f"C{index}", "Concluído")
    ss.update_acell(f"H{index}", end_task["difficulty"])
    ss.update_acell(f"I{index}", f"{end_task['row'][8]}\n{end_task['comments']}")

    update.message.reply_text(f"Tarefa {end_task['row'][1]} concluída com sucesso!")
    return ConversationHandler.END


conclude_handler = ConversationHandler(
    entry_points=[CommandHandler("end", conclude_task)],
    states={
        SYSTEM: [MessageHandler(Filters.text & ~(Filters.command), system)],
        SUBSYSTEM: [MessageHandler(Filters.text & ~(Filters.command), subsystem)],
        TASK: [MessageHandler(Filters.text & ~(Filters.command), task)],
        DIFFICULTY: [MessageHandler(Filters.text & ~(Filters.command), difficulty)],
        COMMENTS: [MessageHandler(Filters.text & ~(Filters.command), comments)],
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=30,
)
