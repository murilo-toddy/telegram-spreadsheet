from telegram.ext import CallbackContext, ConversationHandler
from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from .conversation import Conversation
from utils import available_systems, electric_subsystems, mechanics_subsystem


# A dictionary to store information about each conversation, identified by the sender's telegram ID
conversation_task = {}


# Returns keyboard markup based on dictionary
def __create_keyboard(elements: list) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([elements[i::2] for i in range(2)], one_time_keyboard=True)


# System and subsystem default keyboards
keyboards = {
    "system": __create_keyboard(available_systems),
    "subsystem": {
        "ele": __create_keyboard(list(electric_subsystems.keys())),
        "mec": __create_keyboard(list(mechanics_subsystem.keys())),
    }
}


# Instantiates a new conversation based on sender's username
def load_conversation(update: Update) -> None:
    conversation_task[update.effective_user.username] = Conversation()


# Returns a dictionary containing all info of a certain conversation
def get_conversation(update: Update) -> Conversation:
    return conversation_task[update.effective_user.username]


# Returns standardized string to begin conversation stage
def get_default_system_message(mode: str, description: str) -> str:
    return (
        f"<b>{mode}</b>\n"
        f"{description}\n\n"
        "Utilize <code>/cancel</code> a qualquer momento para cancelar a operação\n"
        "Informe o sistema"
    )


# Function executed whenever a timeout occurs
def timeout(update: Update, ctx: CallbackContext) -> int:
    update.message.reply_text(
        "Limite de tempo excedido\nInicie o processo novamente", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Function executed whenever a conversation is cancelled
def cancel(update: Update, ctx: CallbackContext) -> int:
    update.message.reply_text("Processo cancelado", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
