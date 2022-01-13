from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram import Update, ParseMode
from spreadsheet import ss
from utils import subsystems
import itertools
import commands.handler as handler
import commands.subsystems.task_list as task_list

available_functions = ["l", "i", "c", "a"]


def bt(update: Update, ctx: CallbackContext) -> None:
    subsystem_generic(update, ctx, "bt")

def pt(update: Update, ctx: CallbackContext) -> None:
    subsystem_generic(update, ctx, "pt")

def hw(update: Update, ctx: CallbackContext) -> None:
    subsystem_generic(update, ctx, "hw")

def sw(update: Update, ctx: CallbackContext) -> None:
    subsystem_generic(update, ctx, "sw")


def function_manager(update: Update, ctx: CallbackContext, sub: str, function: str, args=None) -> None:
    if function == "l":
        task_list.subsystem_task_lister(update, ctx, sub, args)

    elif function == "i":
        print("start task")
    
    elif function == "c": 
        print("conclude task")

    elif function == "a":
        print("add task")


def get_default_text(sub: str) -> str:
    return (
        f"<b>Subsistema: {subsystems[sub]['name']}</b>\n"
        f"<u>Tarefas:</u> {len(ss.sheet(sub).get_all_values()[1:])}\n\n"
        "<u>Funções</u>\n"
        f"<code>/{sub} l</code> Listar tarefas\n"
        f"<code>/{sub} i</code> Iniciar tarefa\n"
        f"<code>/{sub} c</code> Concluir tarefa\n"
        f"<code>/{sub} a</code> Adicionar tarefa\n\n"
        "<u>Ações Rápidas</u> (Tarefas)"
    )


def subsystem_generic(update: Update, ctx: CallbackContext, sub: str) -> None:
    handler.log_command(sub)
    
    if not ctx.args:
        buttons = [
            [InlineKeyboardButton("Listar",    callback_data=f"{sub} l"),
             InlineKeyboardButton("Adicionar", callback_data=f"{sub} a")], 
            [InlineKeyboardButton("Concluir",  callback_data=f"{sub} c"),
             InlineKeyboardButton("Iniciar",   callback_data=f"{sub} i")],
        ]
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=get_default_text(sub), 
                            reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)

    else:
        function = ctx.args[0]
        args = " ".join(ctx.args[1:])

        if function not in available_functions:
            update.message.reply_text(get_default_text(sub), parse_mode=ParseMode.HTML)

        else:
            function_manager(update, ctx, sub, function, args)


def query_handler(update: Update, ctx: CallbackContext) -> None:
    query = update.callback_query.data
    cartesian = itertools.product(subsystems.keys(), available_functions)
    options = list(map(lambda e: " ".join(e), cartesian))

    if query in options:    
        update.callback_query.answer()
        [sub, func] = query.split(" ")
        function_manager(update, ctx, sub, func)
