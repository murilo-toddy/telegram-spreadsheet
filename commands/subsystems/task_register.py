# TODO
# Fix document adding bug
# Add comment option
# Add project name and merging
# Export similar functions to other module
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)
from unidecode import unidecode

from spreadsheet import systems
from .generic import get_default_system_message, timeout, cancel, load_conversation, get_conversation
from ..general import log_command

# States of conversation
[
    SYSTEM,
    SUBSYSTEM,
    PROJECT,
    TASK,
    DIFFICULTY,
    DURATION,
    DOC_QUESTION,
    DOCUMENTS,
    CONFIRMATION,
] = range(9)


# TODO extract all message sending commands to generic file
def add_task(update: Update, ctx: CallbackContext) -> int:
    log_command("register task")
    load_conversation(update)
    system_selector = [["ele", "mec"]]
    update.message.reply_text(
        get_default_system_message("Adicionar tarefa", "Adiciona uma nova tarefa na planilha de mapeamento do sistema"),
        reply_markup=ReplyKeyboardMarkup(system_selector, one_time_keyboard=True),
        parse_mode=ParseMode.HTML,
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


def get_active_projects(update: Update) -> str:
    conversation = get_conversation(update)
    ss = conversation.ss.sheet(conversation.subsystem)
    data = ss.get_all_values()
    projects = [f"{index+1} - {row[0]}" for index, row in enumerate(row for row in data if row[0])]

    conversation.projects = projects
    return "\n".join(projects)


def subsystem(update: Update, ctx: CallbackContext) -> int:
    subsystem = update.message.text

    conversation = get_conversation(update)
    conversation.subsystem = subsystem

    reply_text = (
        f"<b>Subsistema: {conversation.dict[subsystem]['name']}</b>\n\n"
        "Para adicionar a tarefa a um projeto existente, forneça seu número\n"
        "Para adicionar um novo projeto, insira o nome deste "
        "(capitalização e acentuação são importantes)\n\n"
        f"<u>Projetos Ativos</u>\n{get_active_projects(update)}"
    )

    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    return PROJECT


def project(update: Update, ctx: CallbackContext) -> int:
    project = update.message.text

    conversation = get_conversation(update)

    try:
        project_number = int(project)
        conversation.new_project = False
        conversation.project = conversation.projects[project_number - 1].split(" - ")[1]

    except:
        conversation.new_project = True
        conversation.project = project

    update.message.reply_text(
        f"Projeto {conversation.project} selecionado\n"
        "Insira o nome da tarefa\n"
        "Capitalização e acentuação são importantes",
    )
    return TASK


def task(update: Update, ctx: CallbackContext) -> int:
    conversation = get_conversation(update)
    conversation.task = update.message.text
    update.message.reply_text("Forneça uma estimativa (0 - 10) para a dificuldade desta tarefa")
    return DIFFICULTY


def difficulty(update: Update, ctx: CallbackContext) -> int:
    try:
        difficulty = float(update.message.text)
        if difficulty < 0 or difficulty > 10:
            raise Exception

    except:
        update.message.reply_text("Entrada inválida!\n\nA dificuldade deve ser um número entre 1 e 10")
        return DIFFICULTY

    conversation = get_conversation(update)
    conversation.difficulty = difficulty
    update.message.reply_text("Forneça uma estimativa de tempo (em semanas) para a realização desta tarefa")
    return DURATION


def duration(update: Update, ctx: CallbackContext) -> int:
    try:
        dur = float(update.message.text)
        if dur < 0:
            raise Exception
    except:
        update.message.reply_text("Entrada inválida!\n\nForneça um número positivo")
        return DURATION

    conversation = get_conversation(update)
    conversation.duration = dur

    question = [["Sim", "Não"]]
    update.message.reply_text(
        "Gostaria de associar esta tarefa a algum documento?",
        reply_markup=ReplyKeyboardMarkup(question, one_time_keyboard=True),
    )
    return DOC_QUESTION


def documents_question(update: Update, ctx: CallbackContext) -> int:
    answer = unidecode(update.message.text.lower())
    if answer == "sim":
        update.message.reply_text("Forneça o link para o(s) documento(s)", reply_markup=ReplyKeyboardRemove())
        return DOCUMENTS


def documents(update: Update, ctx: CallbackContext) -> int:
    conversation = get_conversation(update)
    conversation.documents = update.message.text if unidecode(update.message.text.lower()) != "nao" else ""

    question = [["Sim", "Não"]]
    update.message.reply_text(
        "<b>Confirme as informações</b>\n\n"
        f"<i>Subsistema:</i> {conversation.dict[conversation.subsystem]['name']}\n"
        f"<i>Projeto:</i> {conversation.project}\n"
        f"<i>Tarefa:</i> {conversation.task}\n"
        f"<i>Dificuldade:</i> {conversation.difficulty}\n"
        f"<i>Duração:</i> {conversation.duration}\n\n"
        "Deseja adicionar a tarefa?",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(question, one_time_keyboard=True),
    )
    return CONFIRMATION


def confirmation(update: Update, ctx: CallbackContext) -> int:
    answer = unidecode(update.message.text.lower())
    if answer == "sim":
        conversation = get_conversation(update)
        conversation.ss.register_task(conversation)
        update.message.reply_text("Tarefa adicionada com sucesso", reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text("Processo cancelado", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


register_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add_task)],
    states={
        SYSTEM: [MessageHandler(Filters.text & ~Filters.command, system)],
        SUBSYSTEM: [MessageHandler(Filters.text & ~Filters.command, subsystem)],
        PROJECT: [MessageHandler(Filters.text & ~Filters.command, project)],
        TASK: [MessageHandler(Filters.text & ~Filters.command, task)],
        DIFFICULTY: [MessageHandler(Filters.text & ~Filters.command, difficulty)],
        DURATION: [MessageHandler(Filters.text & ~Filters.command, duration)],
        DOC_QUESTION: [MessageHandler(Filters.text & ~Filters.command, documents_question)],
        DOCUMENTS: [MessageHandler(Filters.text & ~Filters.command, documents)],
        CONFIRMATION: [MessageHandler(Filters.text & ~Filters.command, confirmation)],
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=30,
)
