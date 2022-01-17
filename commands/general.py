from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from spreadsheet import commands, SHEET_URL

def send_sheet(update: Update, ctx: CallbackContext) -> None:
    ctx.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f'<a href="{SHEET_URL}">Planilha de Planejamento</a>',
        parse_mode=ParseMode.HTML
    )


def spreadsheet_return_text(update: Update, ctx: CallbackContext) -> None:
    cmd = update.message.text[1:]
    l = [ cmds[0] for cmds in commands.sheet("cmd").get_all_values()[1:] ]
    print(f"[!!] Command {cmd} called")
    
    index = l.index(cmd) + 1
    ctx.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=commands.sheet("cmd").get_all_values()[index][1],
        parse_mode=ParseMode.HTML
    )
