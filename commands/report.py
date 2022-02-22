from telegram import Update
from telegram.ext import CallbackContext

from config import REPORT_CHAT_ID
from database.connection import Connection
from .general import send_message, send_message_to
from .help import available_commands


def list_reports(update: Update, ctx: CallbackContext):
    if len(ctx.args) > 1 and ctx.args[1] == "all":
        query = "SELECT * FROM report;"
    else:
        query = "SELECT * FROM report WHERE fixed = false;"
    if reports := Connection().exec(query, func=lambda cur: cur.fetchall()):
        send_message(update, ctx, f"<u>Reports abertos</u> ({len(reports)})")
        for index, report in enumerate(reports):
            report_text = (
                f"Report {index + 1}\n"
                f"<b>Comando:</b> {report[1]}\n"
                f"<b>Corrigido:</b> {'Sim' if report[3] else 'Não'}\n"
                f"<b>Responsável:</b> @{report[0]}\n"
                f"<b>Problema:</b>\n{report[2]}\n\n"
                "Deseja corrigir o report?"
            )
            send_message(update, ctx, report_text)
    else:
        send_message(update, ctx, "Não há reports para apresentar")


def fix_report(update: Update, ctx: CallbackContext):
    query = "SELECT * FROM report WHERE fixed = false;"
    open_reports = Connection().exec(query, func=lambda cur: cur.fetchall())
    error_reply = (
        f"O report inserido não foi encontrado. Atualmente há {len(open_reports)} abertos.\n"
        "Lembre-se de utilizar a sintaxe <code>/report fix [número do report]</code>\n\n"
        "Todos os reports podem ser observados através do comando <code>/report list</code>"
    )
    try:
        if len(ctx.args) < 2 or len(open_reports) < int(ctx.args[1]) or int(ctx.args[1]) < 1:
            send_message(update, ctx, error_reply)
        else:
            report = open_reports[int(ctx.args[1]) - 1]
            report_text = (
                f"Report {ctx.args[1]}\n"
                f"<b>Comando:</b> {report[1]}\n"
                f"<b>Corrigido:</b> {'Sim' if report[3] else 'Não'}\n"
                f"<b>Responsável:</b> @{report[0]}\n"
                f"<b>Problema:</b>\n{report[2]}"
            )
            print(report_text)

    except ValueError:
        send_message(update, ctx, error_reply)


def report_chat_handler(update: Update, ctx: CallbackContext):
    if not ctx.args or ctx.args[0] == "list":
        list_reports(update, ctx)
    elif ctx.args[0] == "fix":
        fix_report(update, ctx)


# Command that enables users to report malfunctions
def report_command(update: Update, ctx: CallbackContext):
    if int(update.effective_chat.id) == int(REPORT_CHAT_ID):
        report_chat_handler(update, ctx)

    elif not ctx.args:
        reply_text = (
            "Você deve fornecer uma mensagem de report.\n\n"
            "Para reportar um problema utilize:\n"
            "<code>/report [comando] problema</code>"
        )
        send_message(update, ctx, reply_text)
        return

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
            "<u>Novo report</u>\n"
            f"<b>Responsável:</b> @{update.effective_user.username}\n"
            f"<b>Comando:</b> {cmd}\n"
            f"<b>Problema:</b>\n{message}"
        )
        query = "INSERT INTO report(author, command, message, fixed) VALUES(%s, %s, %s, False);"
        Connection().exec_and_commit(query, update.effective_user.username, cmd, message)
        send_message_to(ctx, REPORT_CHAT_ID, report_message)
