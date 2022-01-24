from telegram.ext import CallbackContext, ConversationHandler
from telegram import ReplyKeyboardRemove, Update


def get_default_system_message(mode: str) -> str:
    return (
        f"<b>{mode}</b>\n"
        "Utilize <code>/cancel</code> a qualquer momento para cancelar a operação\n"
        "Informe o sistema"
    )


def timeout(update: Update, ctx: CallbackContext):
    update.message.reply_text(
        "Limite de tempo excedido\nInicie o processo novamente", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def cancel(update: Update, ctx: CallbackContext) -> int:
    update.message.reply_text("Processo cancelado", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
