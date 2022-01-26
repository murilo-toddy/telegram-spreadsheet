from telegram.ext import CallbackContext, ConversationHandler
from telegram import ReplyKeyboardRemove, Update

# A dictionary to store information about each conversation, identified by the sender's telegram ID
conversation_task = {}


def get_default_system_message(mode: str) -> str:
    return (
        f"<b>{mode}</b>\n"
        "Utilize <code>/cancel</code> a qualquer momento para cancelar a operação\n"
        "Informe o sistema"
    )


# Function executed whenever a timeout occours
def timeout(update: Update, ctx: CallbackContext):
    update.message.reply_text(
        "Limite de tempo excedido\nInicie o processo novamente", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Function executed whenever a conversation is cancelled
def cancel(update: Update, ctx: CallbackContext) -> int:
    update.message.reply_text("Processo cancelado", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
