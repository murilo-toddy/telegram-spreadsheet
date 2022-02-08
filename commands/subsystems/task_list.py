from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ..general import send_message
from spreadsheet import systems


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
    if system == "ele":
        name = systems["ele"]["sub"][subsystem]["name"]
        ss = systems["ele"]["ss"].sheet(subsystem)
    else:
        name = systems["mec"]["sub"][subsystem]["name"]
        ss = systems["mec"]["ss"].sheet(subsystem)

    data = ss.get_all_values()
    string = f"<b>Subsistema: {name}</b>\n\n<u>Tarefas</u>\n"
    counter = 1

    for i in range(1, len(data)):
        if data[i][0]:
            tasks, pos, counter = get_subtasks(data, i, counter)
            if tasks:
                string += f"\n<i>{data[i][0]}</i>\n" + tasks
            i = pos

    return string


def task_lister(update: Update, ctx: CallbackContext, args: list[str]) -> None:
    sub = args[0].strip().lower()
    if sub == "ele":
        subsystems = [
            [
                InlineKeyboardButton("Baterias", callback_data="list bt"),
                InlineKeyboardButton("Powertrain", callback_data="list pt"),
            ],
            [
                InlineKeyboardButton("Hardware", callback_data="list hw"),
                InlineKeyboardButton("Software", callback_data="list sw"),
            ],
        ]
        ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text="<b>Elétrica</b>\n\n"
            "O sistema da elétrica possui os seguintes subsistemas:\n"
            "- Baterias\n- Powertrain\n- Hardware\n- Software\n\n"
            "Escolha o subsistema que deseja listar as tarefas",
            reply_markup=InlineKeyboardMarkup(subsystems),
            parse_mode=ParseMode.HTML,
        )

    elif sub == "mec":
        subsystems = [[InlineKeyboardButton("Chassi", callback_data="list ch")]]
        ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text="<b>Mecânica</b>\n\n"
            "O sistema da mecânica possui os seguintes subsistemas:\n"
            "- Chassi\n\n"
            "Escolha o subsistema que deseja listar as tarefas",
            reply_markup=InlineKeyboardMarkup(subsystems),
            parse_mode=ParseMode.HTML,
        )

    elif sub in systems["ele"]["sub"].keys():
        send_message(update, ctx, get_task_lister_text("ele", sub))

    elif sub in systems["mec"]["sub"].keys():
        send_message(update, ctx, get_task_lister_text("mec", sub))

    else:
        send_message(update, ctx, "Sistema ou subsistema não encontrado")


def subsystem_task_lister(update: Update, ctx: CallbackContext) -> None:
    if args := ctx.args:
        task_lister(update, ctx, args)
    else:
        systems = [
            [
                InlineKeyboardButton("Elétrica", callback_data="list ele"),
                InlineKeyboardButton("Mecânica", callback_data="list mec"),
            ]
        ]
        ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Escolha um sistema ou subsistema\n\n<code>/list &lt;subsistema&gt;</code>",
            reply_markup=InlineKeyboardMarkup(systems),
            parse_mode=ParseMode.HTML,
        )


def query_handler(update: Update, ctx: CallbackContext) -> None:
    """
    Handler responsible to call list function when buttons
    are pressed
    """
    query = update.callback_query.data
    [cmd, *args] = query.split(" ")

    if cmd == "list":
        task_lister(update, ctx, args)
