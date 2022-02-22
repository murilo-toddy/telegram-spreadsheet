from telegram import Update
from telegram.ext import CallbackContext

from commands.general import log_command, send_message


# TODO change dictrionary for dataclass
# Helper function to create dictionary with specific keys
def _create_command_dict(category: str, short_description: str, full_description: str):
    return {
        "category": category,
        "short_description": short_description,
        "full_description": full_description,
    }


# Dictionary containing available commands
available_commands = {
    "help": _create_command_dict(
        category="Geral",
        short_description="Fornece informação sobre comandos disponíveis",
        full_description=(
            "Lista informações a respeito dos comandos disponíveis, divididos por categoria.\n\n"
            "Informações a respeito de um comando específico podem ser obtidas utilizando "
            "<code>/help &lt;comando&gt;</code>."
        ),
    ),
    "planilha": _create_command_dict(
        category="Geral",
        short_description="Retorna a planilha de comandos",
        full_description=(
            "Envia o link da planilha de comandos do Tupão\n"
            "Para cadastrar um novo comando, basta inserir este e a resposta "
            "de texto esperada na ultima linha.\n"
            "Para formatações específicas no texto de resposta, use tags <i>HTML</i>\n\n"
            "Após inserção do comando na planilha, execute o comando <code>/refresh</code>"
            "para atualizar os comandos internos do Bot."
        ),
    ),
    "report": _create_command_dict(
        category="Geral",
        short_description="Reporte comandos ou problemas no bot",
        full_description=(
            "Permite que o usuário informe os desenvolvedores a respeito de problemas no bot\n\n"
            "Ao enviar um report, sua reclamação será salva em um banco de dados para que seja analisada "
            "pelos responsáveis. Só é necessário reportar um problema <b>uma vez</b>\n\n"
            "Para reportar um novo problema, utilize <code>/report [comando] problema</code>\n"
            "É importante ressaltar que o comando deve ser exatamente como apresentado no <code>/help</code>\n\n"
            "Fique atento aos <i>patch notes</i> do bot para saber das ultimas atualizações."
        )
    ),
    "list": _create_command_dict(
        category="Subsistemas",
        short_description="Lista as tarefas de um subsistema",
        full_description=(
            "Lista todas as tarefas não concluídas de um subsistema, com base na planilha "
            "de atividades deste.\n\n"
            "As tarefas são listadas separadas por projeto\n\n"
            "É possível executar <code>/list &lt;subsistema&gt;</code> para "
            "obter informações de um subsistema imediatamente. O subsistema deve ser fornecido "
            "através de sua abreviação (i.e. <code>/list sw</code>).\n\n"
            "Por outro lado, pode-se utilizar <code>/list</code> sem argumentos para receber "
            "uma lista com os sistemas e subsistemas disponíveis."
        ),
    ),
    "add": _create_command_dict(
        category="Subsistemas",
        short_description="Adiciona uma nova tarefa",
        full_description=(
            "Adiciona uma nova tarefa na planilha de atividades do sistema\n\n"
            "Ao selecionar o subsistema, o bot responderá com a lista de projetos ativos.\n"
            "É possível então selecionar um dos projetos já existentes através de seu número ou "
            "criar um projeto totalmente novo, fornecendo seu nome.\n"
            "Em seguida, serão realizadas perguntas a respeito da atividade a ser incluída.\n\n"
            "Ao finalizar a conversa com o bot, a nova atividade será adicionada imediatamente na planilha "
            "de atividades do sistema.\n\n"
            "É possível executar <code>/add &lt;subsistema&gt;</code> para "
            "selecionar um subsistema imediatamente. O subsistema deve ser fornecido "
            "através de sua abreviação (i.e. <code>/add sw</code>).\n\n"
            "Por outro lado, pode-se utilizar <code>/add</code> sem argumentos para receber "
            "uma lista com os sistemas e subsistemas disponíveis."
        ),
    ),
    "init": _create_command_dict(
        category="Subsistemas",
        short_description="Inicia uma tarefa",
        full_description=(
            "Muda o status de uma tarefa da planilha de atividades do sistema para Fazendo\n\n"
            "Ao selecionar o subsistema, o bot responderá com a lista de tarefas ativas. Ao selecionar "
            "a desejada, esta terá seu status atualizado automaticamente na planilha.\n\n"
            "É possível executar <code>/start &lt;subsistema&gt;</code> para "
            "obter as tarefas de um subsistema imediatamente. O subsistema deve ser fornecido "
            "através de sua abreviação (i.e. <code>/start sw</code>).\n\n"
            "Por outro lado, pode-se utilizar <code>/start</code> sem argumentos para receber "
            "uma lista com os sistemas e subsistemas disponíveis."
        ),
    ),
    "end": _create_command_dict(
        category="Subsistemas",
        short_description="Conclui uma tarefa",
        full_description=(
            "Muda o status de uma tarefa da planilha de atividades do sistema para Concluído\n\n"
            "Ao selecionar o subsistema, o bot responderá com a lista de tarefas ativas. Ao selecionar "
            "a desejada, serão realizadas algumas perguntas a respeito do desenvolvimento desta, que "
            "serão automaticamente adicionadas na planilha.\n\n"
            "É possível executar <code>/end &lt;subsistema&gt;</code> para "
            "obter as tarefas de um subsistema imediatamente. O subsistema deve ser fornecido "
            "através de sua abreviação (i.e. <code>/end sw</code>).\n\n"
            "Por outro lado, pode-se utilizar <code>/end</code> sem argumentos para receber "
            "uma lista com os sistemas e subsistemas disponíveis."
        ),
    ),
}


# TODO show commands separated by category
# Returns description with all available commands
def get_default_description() -> str:
    string = "<b>Comandos disponíveis</b>\n\n"
    for cmd, info in available_commands.items():
        string += f"/{cmd} - {info['short_description']}\n"

    string += "\nUtilize <code>/help &lt;comando&gt;</code> para obter ajuda para um comando específico"
    return string


# Returns help for specified command as stated in dictionary
def get_personalized_description(command: str) -> str:
    return f"<b>Comando {command}</b>\n\n<u>Descrição</u>\n{available_commands[command]['full_description']}"


def help_command(update: Update, ctx: CallbackContext) -> None:
    """
    Help command method
    Returns a list of available commands if no argument is specified
    Returns help for specific command otherwise
    """
    log_command("help")
    if ctx.args and ctx.args[0] in available_commands.keys():
        send_message(update, ctx, get_personalized_description(ctx.args[0]))

    else:
        send_message(update, ctx, get_default_description())
