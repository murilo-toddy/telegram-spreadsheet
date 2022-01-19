from typing import NewType
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove,
    ParseMode
)
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext, 
    ConversationHandler
)
from utils import ele_subsystems, mec_subsystems
from spreadsheet import ele_ss, mec_ss
from commands.handler import log_command
import unidecode


SYSTEM, SUBSYSTEM, PROJECT, TASK, DIFFICULTY, DURATION, DOC_QUESTION, DOCUMENTS = range(8)

task_info = {
    "system": "",
    "subsystem": "",
    "project": "",
    "new_project": False,
    "task": "",
    "diff": "",
    "duration": "",
    "docs": "",
}
new_task = { "ss": None, "dict": None, "task": task_info, "proj": "" }


def add_task(update: Update, ctx: CallbackContext) -> int:
    log_command("add task")
    system_selector = [[ "ele", "mec" ]]
    update.message.reply_text(
        "<b>Adicionar tarefa</b>\n"
        "Utilize <code>/cancel</code> a qualquer momento para cancelar a operação\n\n"
        "Informe o sistema\n",
        reply_markup=ReplyKeyboardMarkup(
            system_selector, one_time_keyboard=True
        ),
        parse_mode=ParseMode.HTML
    )
    return SYSTEM


def system(update: Update, ctx: CallbackContext) -> int:
    system = update.message.text
    if   system == "ele": subsystem_selector = [[ "bt", "pt" ], [ "hw", "sw" ]]
    elif system == "mec": subsystem_selector = [[ "ch" ]]
    else:
        update.message.reply_text("Sistema não encontrado", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    
    global new_task
    new_task["task"]["system"] = system
    new_task["dict"] = ele_subsystems if system == "ele" else mec_subsystems
    new_task["ss"] = ele_ss if system == "ele" else mec_ss

    update.message.reply_text(
        "Informe o subsistema",
        reply_markup=ReplyKeyboardMarkup(
            subsystem_selector, one_time_keyboard=True
        ),
        parse_mode=ParseMode.HTML
    )
    return SUBSYSTEM


def get_active_projects() -> str:
    global new_task
    ss = new_task["ss"].sheet(new_task["task"]["subsystem"])
    data = ss.get_all_values()
    projects = [f"{index+1} - {row[0]}" 
                    for index, row in enumerate(row 
                        for row in data if row[0])]
    
    new_task["proj"] = projects
    return "\n".join(projects)


def subsystem(update: Update, ctx: CallbackContext) -> int:
    subsystem = update.message.text
    global new_task
    new_task["task"]["subsystem"] = subsystem
    reply_text = (
        f"<b>Subsistema: {new_task['dict'][subsystem]['name']}</b>\n\n"
        "Para adicionar a tarefa a um projeto existente, forneça seu número\n"
        "Para adicionar um novo projeto, insira o nome deste "
        "(capitalização e acentuação são importantes)\n\n"
        f"<u>Projetos Ativos</u>\n{get_active_projects()}"
    )

    update.message.reply_text(
        reply_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML
    )
    return PROJECT


def project(update: Update, ctx: CallbackContext) -> int:
    project = update.message.text
    global new_task

    try:
        project_number = int(project)
        new_task["task"]["new_project"] = False
        new_task["task"]["project"] = new_task["proj"][project_number-1].split(" - ")[1]

    except:
        new_task["task"]["project"] = project
        new_task["task"]["new_project"] = True
    
    update.message.reply_text(
        f"Projeto {new_task['task']['project']} selecionado\n"
        "Insira o nome da tarefa"
    )
    return TASK


def task(update: Update, ctx: CallbackContext) -> int:
    global new_task
    new_task["task"]["task"] = update.message.text
    update.message.reply_text("Forneça uma estimativa (0 - 10) para a dificuldade desta tarefa")
    return DIFFICULTY


def difficulty(update: Update, ctx: CallbackContext) -> int:
    try:
        difficulty = float(update.message.text)
        if difficulty < 0 or difficulty > 10: raise Exception

    except:
        update.message.reply_text("Entrada inválida!\n\nA dificuldade deve ser um número entre 1 e 10")
        return DIFFICULTY

    global new_task
    new_task["task"]["diff"] = difficulty
    update.message.reply_text("Forneça uma estimativa de tempo (em semanas) para a realização desta tarefa")
    return DURATION


def duration(update: Update, ctx: CallbackContext) -> int:
    try:
        dur = float(update.message.text)
        if dur < 0: raise Exception
    except:
        update.message.reply_text("Entrada inválida!\n\nForneça um número positivo")
        return DURATION
    
    global new_task
    new_task["task"]["dur"] = dur
    question = [[ "Sim", "Não" ]]
    update.message.reply_text(
        "Gostaria de associar esta tarefa a algum documento?",
        reply_markup=ReplyKeyboardMarkup(
            question, one_time_keyboard=True
        )
    )
    return DOCUMENTS


def documents_question(update: Update, ctx: CallbackContext) -> int:
    answer = unidecode.unidecode(update.message.text.lower())
    if answer == "sim":
        update.message.reply_text("Forneça o link para o(s) documento(s)")
    return DOCUMENTS


def documents(update: Update, ctx: CallbackContext) -> int:
    global new_task
    new_task["task"]["docs"] = update.message.text
    update.message.reply_text(
        "<b>Tarefa Adicionada</b>\n\n"
        f"<i>Subsistema:</i> {new_task['dict'][new_task['task']['subsystem']]['name']}\n"
        f"<i>Projeto:</i> {new_task['task']['project']}\n"
        f"<i>Tarefa:</i> {new_task['task']['task']}\n"
        f"<i>Dificuldade:</i> {new_task['task']['diff']}\n"
        f"<i>Duração:</i> {new_task['task']['dur']}\n",
        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def cancel(update: Update, ctx: CallbackContext) -> int:
    update.message.reply_text("Processo cancelado")
    return ConversationHandler.END



register_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_task)],
        states={
            SYSTEM:       [ MessageHandler(Filters.text & ~(Filters.command), system)             ],
            SUBSYSTEM:    [ MessageHandler(Filters.text & ~(Filters.command), subsystem)          ],
            PROJECT:      [ MessageHandler(Filters.text & ~(Filters.command), project)            ],
            TASK:         [ MessageHandler(Filters.text & ~(Filters.command), task)               ],
            DIFFICULTY:   [ MessageHandler(Filters.text & ~(Filters.command), difficulty)         ],
            DURATION:     [ MessageHandler(Filters.text & ~(Filters.command), duration)           ],
            DOC_QUESTION: [ MessageHandler(Filters.text & ~(Filters.command), documents_question) ],
            DOCUMENTS:    [ MessageHandler(Filters.text & ~(Filters.command), documents)          ], 
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
