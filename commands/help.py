from telegram import Update
from telegram.ext import CallbackContext
from commands.general import send_message

# Dictionary containing available commands
available_commands = {
    "help": ("Lista informações a respeito dos comandos disponíveis"),
    "planilha": (
        "Envia o link da planilha de comandos do Tupão\n"
        "Para cadastrar um novo comando, basta inserir este e a resposta "
        "de texto esperada na ultima linha.\n"
        "Para formatações específicas no texto de resposta, use tags <i>HTML</i>\n"
        "Após inserção do comando na planilha, execute o comando <code>/refresh</code>"
        "para atualizar os comandos internos do Bot."
    ),
    "list": ("Lista todas as tarefas não concluídas de um subsistema"),
    "add": ("Adiciona uma nova tarefa na planilha"),
    "start": ("Muda o status de uma tarefa para Em Andamento"),
    "end": ("Muda o status de uma tarefa para finalizado"),
}


def get_default_description() -> str:
    return (
        "<b>Comandos disponíveis</b>\n"
        f"<code>{'</code>, <code>'.join(available_commands.keys())}</code>.\n\n"
        "Utilize <code>/help &lt;comando&gt;</code> para obter ajuda para um comando específico"
    )


def get_personalized_description(command: str) -> str:
    return f"<b>Comando {command}</b>\n\n<u>Descrição</u>\n{available_commands[command]}"


def help_command(update: Update, ctx: CallbackContext):
    if ctx.args and ctx.args[0] in available_commands.keys():
        send_message(update, ctx, get_personalized_description(ctx.args[0]))

    else:
        send_message(update, ctx, get_default_description())
