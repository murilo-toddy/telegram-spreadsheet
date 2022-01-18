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
import commands.general as general


SYSTEM, SUBSYSTEM, PROJECT, TASK, DIFFICULTY, DURATION, DOCUMENTS = range(7)

task = {
    "system": "",
    "subsystem": "",
    "project": "",
    "task": "",
    "diff": "",
    "duration": "",
    "docs": "",
}
new_task = {
    "ss": None,
    "dict": None,
    "task": task
}

def add_task(update: Update, ctx: CallbackContext):
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


def system(update: Update, ctx: CallbackContext):
    system = update.message.text
    if system == "ele":   subsystem_selector = [[ "bt", "pt" ], [ "hw", "sw" ]]
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
    print(ss)
    return 0



def subsystem(update: Update, ctx: CallbackContext):
    subsystem = update.message.text
    global new_task
    new_task["task"]["subsystem"] = subsystem
    
    update.message.reply_text(
        f"<b>Subsistema: {new_task['dict'][subsystem]['name']}</b>\n\n"
        f"<u>Projetos Ativos</u>\n{get_active_projects()}",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML
    )
    
    print(f"selected {update.message.text}")
    return PROJECT

def project(update: Update, ctx: CallbackContext):
    user = update.message.from_user
    update.message.reply_text("projeto")
    print(f"{user.first_name} selected {update.message.text}")
    return TASK

def task(update: Update, ctx: CallbackContext):
    user = update.message.from_user
    update.message.reply_text("tarefa")
    print(f"{user.first_name} selected {update.message.text}")
    return DIFFICULTY

def difficulty(update: Update, ctx: CallbackContext):
    user = update.message.from_user
    update.message.reply_text("diff")
    print(f"{user.first_name} selected {update.message.text}")
    return DURATION

def duration(update: Update, ctx: CallbackContext):
    user = update.message.from_user
    update.message.reply_text("dur")
    print(f"{user.first_name} selected {update.message.text}")
    return DOCUMENTS

def documents(update: Update, ctx: CallbackContext):
    user = update.message.from_user
    update.message.reply_text("doc")
    print(f"{user.first_name} selected {update.message.text}")
    return ConversationHandler.END


def cancel(update: Update, ctx: CallbackContext):
    update.message.reply_text("Processo cancelado")
    return ConversationHandler.END



register_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_task)],
        states={
            SYSTEM:     [ MessageHandler(Filters.text & ~(Filters.command), system)     ],
            SUBSYSTEM:  [ MessageHandler(Filters.text & ~(Filters.command), subsystem)  ],
            PROJECT:    [ MessageHandler(Filters.text & ~(Filters.command), project)    ],
            TASK:       [ MessageHandler(Filters.text & ~(Filters.command), task)       ],
            DIFFICULTY: [ MessageHandler(Filters.text & ~(Filters.command), difficulty) ],
            DURATION:   [ MessageHandler(Filters.text & ~(Filters.command), duration)   ],
            DOCUMENTS:  [ MessageHandler(Filters.text & ~(Filters.command), documents)  ], 
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
