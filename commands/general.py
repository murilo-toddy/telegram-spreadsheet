from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from spreadsheet import commands
from config import COMMANDS_SHEET_ID
import bot


# Registers execution of certain command
def log_command(cmd: str) -> None:
    print(f"\n  [!!] Command {cmd} called")


# Default message senting method, using HTML format
def send_message(update: Update, ctx: CallbackContext, text: str) -> None:
    ctx.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


# Gets text from commands listed in Bot Commands spreadsheet
def spreadsheet_return_text(update: Update, ctx: CallbackContext) -> None:
    cmd = update.message.text[1:]
    cmds = [cmds[0] for cmds in commands.sheet("cmd").get_all_values()[1:]]
    print(f"[!!] Command {cmd} called")
    index = cmds.index(cmd) + 1
    send_message(update, ctx, commands.sheet("cmd").get_all_values()[index][1])


# Reload commands listed in Bot Commands spreadsheet
def update_sheet_commands(update: Update, ctx: CallbackContext) -> None:
    bot.handler.register_commands(bot.dsp)
    send_message(update, ctx, "Comandos atualizados com sucesso!")


# Sends Bot Commands spreadsheet link
def send_sheet(update: Update, ctx: CallbackContext) -> None:
    send_message(
        update,
        ctx,
        (
            f"<a href='https://docs.google.com/spreadsheets/d/{COMMANDS_SHEET_ID}/edit#gid=0'>"
            "Planilha de Comandos</a>"
        ),
    )
