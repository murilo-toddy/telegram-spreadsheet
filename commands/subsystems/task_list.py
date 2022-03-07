from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from config import systems
from .generic import get_task_lister_text
from ..general import send_message, log_command


# Shortens inline keyboard creation process
def __create_keyboard(button_name: str, callback: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(button_name, callback_data=callback)


# Sends a message with an inline keyboard associated
def __reply_keyboard(update: Update, ctx: CallbackContext, text: str, keyboard: InlineKeyboardMarkup) -> None:
    ctx.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


# System or subsystem selector
def task_lister(update: Update, ctx: CallbackContext, args: list[str]) -> None:
    log_command("list task")
    sub = args[0].strip().lower()

    if sub == "ele":
        # Electric subsystems lister
        subsystems = [
            [__create_keyboard("Baterias", "list bat"), __create_keyboard("Powertrain", "list pt")],
            [__create_keyboard("Hardware", "list hw"), __create_keyboard("Software", "list sw")],
        ]
        reply_message_text = (
            "<b>Elétrica</b>\n\n"
            "O sistema da elétrica possui os seguintes subsistemas:\n"
            "- Baterias\n- Powertrain\n- Hardware\n- Software\n\n"
            "Escolha o subsistema que deseja listar as tarefas"
        )
        __reply_keyboard(update, ctx, reply_message_text, InlineKeyboardMarkup(subsystems))

    elif sub == "mec":
        # Mechanics subsystem lister
        subsystems = [[__create_keyboard("Chassi", "list ch")]]
        reply_message_text = (
            "<b>Mecânica</b>\n\n"
            "O sistema da mecânica possui os seguintes subsistemas:\n"
            "- Chassi\n\n"
            "Escolha o subsistema que deseja listar as tarefas"
        )
        __reply_keyboard(update, ctx, reply_message_text, InlineKeyboardMarkup(subsystems))

    # Subsystem selected
    elif sub in systems["ele"]["sub"].keys():
        send_message(update, ctx, get_task_lister_text("ele", sub))

    elif sub in systems["mec"]["sub"].keys():
        send_message(update, ctx, get_task_lister_text("mec", sub))

    else:
        send_message(update, ctx, "Sistema ou subsistema não encontrado")


# Generic task lister message
def subsystem_task_lister(update: Update, ctx: CallbackContext) -> None:
    # Arguments passed
    if args := ctx.args:
        task_lister(update, ctx, args)

    # System lister
    else:
        reply_message_text = "Escolha um sistema ou subsistema\n\n<code>/list &lt;subsistema&gt;</code>"
        available_systems = [[__create_keyboard("Elétrica", "list ele"), __create_keyboard("Mecânica", "list mec")]]
        __reply_keyboard(update, ctx, reply_message_text, InlineKeyboardMarkup(available_systems))


def query_handler(update: Update, ctx: CallbackContext) -> None:
    """
    Handler responsible to call list function when buttons
    are pressed
    """
    query = update.callback_query.data
    [cmd, *args] = query.split(" ")

    if cmd == "list":
        task_lister(update, ctx, args)
