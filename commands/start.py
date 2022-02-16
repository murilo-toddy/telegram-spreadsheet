from telegram import Update
from telegram.ext import CallbackContext

from .general import reply_text
from .help import get_default_description


# Command called when a new person starts a conversation with the bot
def start(update: Update, ctx: CallbackContext) -> None:
    start_text = (
        "Olá, eu sou o <b>Tupão</b>, o bot do Tupã.\n"
        "Fui desenvolvido com o intuito de automatizar alguns processos e "
        "facilitar a vida das pessoas.\n\n"
        "Atualmente conto com alguns comandos, listados abaixo."
    )
    reply_text(update, f"{start_text}\n\n{get_default_description()}")
