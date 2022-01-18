from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import (
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext, 
    ConversationHandler
)

SUBSYSTEM, PROJECT, TASK, DIFFICULTY, DURATION, DOCUMENTS = range(6)

new_task = {
    "subsystem": "",
    "project": "",
    "task": "",
    "diff": "",
    "duration": "",
    "docs": "",
}

def add_task(update: Update, ctx: CallbackContext):
    subsystem_selector = [[ 'bt', 'pt' ], [ 'hw', 'sw' ]]
    update.message.reply_text(
        "<b>Adicionar tarefa</b>\n"
        "Utilize <code>cancel</code> para cancelar a operação\n\n"
        "Informe o subsistema\n",
        reply_markup=ReplyKeyboardMarkup(
            subsystem_selector, one_time_keyboard=True
        ),
        parse_mode=ParseMode.HTML
    )
    return SUBSYSTEM


def subsystem(update: Update, ctx: CallbackContext):
    user = update.message.from_user
    update.message.reply_text("subsistema")
    print(f"{user.first_name} selected {update.message.text}")
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
        SUBSYSTEM:  [ MessageHandler(Filters.regex('^(bt|pt|hw|sw)$'),  subsystem) ],
        PROJECT:    [ MessageHandler(Filters.text & ~(Filters.command), project) ],
        TASK:       [ MessageHandler(Filters.text & ~(Filters.command), task) ],
        DIFFICULTY: [ MessageHandler(Filters.text & ~(Filters.command), difficulty) ],
        DURATION:   [ MessageHandler(Filters.text & ~(Filters.command), duration) ],
        DOCUMENTS:  [ MessageHandler(Filters.text & ~(Filters.command), documents) ], 
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
