from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from config import systems
from utils import available_systems, electric_subsystems, mechanics_subsystem
from .conversation import Conversation
from ..general import reply_text

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


# System or subsystem lister when starting conversation
# TODO write extraction method
def check_for_system_or_subsystem():
    pass


# Loads configuration and replies text when a system is selected
def load_system_info(update: Update, selected_system: str) -> any:
    keyboard = keyboards["subsystem"][selected_system]
    reply_text(update, f"Sistema {selected_system} selecionado\nInforme o subsistema", keyboard)
    conversation = get_conversation(update)
    conversation.system = selected_system
    conversation.dict = systems[selected_system]["sub"]
    conversation.ss = systems[selected_system]["ss"]


# Loads configuration and replies text when a subsystem is selected
def load_subsystem_info(update: Update, selected_subsystem: str) -> None:
    conversation = get_conversation(update)
    conversation.subsystem = selected_subsystem
    conversation.tasks = get_task_lister_text(conversation.system, selected_subsystem)

    reply_message = (
        f"{conversation.tasks}\n\n"
        "Selecione da lista acima o número da tarefa que deseja executar a ação"
    )
    reply_text(update, reply_message)


# Project and task listing methods
# TODO refactor functions
def get_subtasks(data: list, pos: int, counter: int) -> tuple[str, int, int]:
    tasks = ""
    i = pos
    while i < len(data) and (not data[i][0] or i == pos):
        if data[i][1] and data[i][2] != "Concluído":
            tasks += f"{counter} - {data[i][1]}\n"
            counter += 1
        i += 1
    return tasks, i, counter


def get_task_lister_text(system: str, subsystem: str) -> str:
    name = systems[system]["sub"][subsystem]["name"]
    ss = systems[system]["ss"].sheet(subsystem)

    data = ss.get_all_values()
    string = f"<b>Subsistema: {name}</b>\n\n<u>Tarefas</u>\n"
    counter = 1

    for i in range(1, len(data)):
        if data[i][0]:
            tasks, pos, counter = get_subtasks(data, i, counter)
            if tasks:
                string += f'\n<i>{data[i][0]}</i>\n{tasks}'
            i = pos
    return string


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
