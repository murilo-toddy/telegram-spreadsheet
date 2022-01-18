from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from spreadsheet import commands
import bot


def send_message(update: Update, ctx: CallbackContext, text: str) -> None:
    ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML
    )


# Gets text from commands listed in Bot Commands spreadsheet
def spreadsheet_return_text(update: Update, ctx: CallbackContext) -> None:
    cmd = update.message.text[1:]
    l = [ cmds[0] for cmds in commands.sheet("cmd").get_all_values()[1:] ]
    print(f"[!!] Command {cmd} called")    
    index = l.index(cmd) + 1
    send_message(update, ctx, commands.sheet("cmd").get_all_values()[index][1])


# Reloads commands listed in Bot Commands spreadsheet
def update_sheet_commands(update: Update, ctx: CallbackContext) -> None:
    bot.handler.register_commands(bot.dsp)
    send_message(update, ctx, "Comandos atualizados com sucesso!")