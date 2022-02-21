from telegram import Update
from telegram.ext import CallbackContext

from config import REPORT_CHAT_ID
from .general import send_message, send_message_to
from .help import available_commands

from database.connection import Connection


# Command that enables users to report malfunctions
def report_command(update: Update, ctx: CallbackContext):
    if not ctx.args:
        reply_text = (
            "Você deve fornecer uma mensagem de report.\n\n"
            "Para reportar um problema utilize:\n"
            "<code>/report [comando] problema</code>"
        )
        send_message(update, ctx, reply_text)
        return

    elif ctx.args[0] == "list":
        query = "SELECT * FROM report;"
        reports = Connection().exec(query, func=lambda cur: cur.fetchone())
        if reports:
            send_message(update, ctx, reports)
        else:
            send_message(update, ctx, "Não há reports para apresentar")

    elif ctx.args[0] not in available_commands.keys():
        reply_text = (
            "Comando não encontrado.\n"
            "Utilize <code>/help</code> para ver a lista de comandos disponíveis.\n\n"
            "Sua mensagem de report deve ter o formato\n"
            "<code>/report [comando] problema</code>"
        )
        send_message(update, ctx, reply_text)
        return

    else:
        cmd = ctx.args[0]
        message = " ".join(ctx.args[1:])
        send_message(update, ctx, "Report enviado com sucesso\nObrigado pela contribuição")
        report_message = (
            "<u>Novo report</u>\n\n"
            f"<b>Responsável:</b> {update.effective_user.username}\n"
            f"<b>Comando:</b> {cmd}\n"
            f"<b>Problema:</b>\n{message}\n"
        )
        query = "INSERT INTO report(author, command, message) " \
                "VALUES(%s, %s, %s);"
        Connection().exec_and_commit(query, update.effective_user.username, cmd, message)
        send_message_to(ctx, REPORT_CHAT_ID, report_message)
