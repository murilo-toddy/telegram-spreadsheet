from spreadsheet import ss
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

def log_command(cmd: str): print(f"[!!] Command {cmd} called")

def register_commands(dsp):
    dsp.add_handler(CommandHandler("sw", sw))


def sw(update: Update, ctx: CallbackContext) -> None:
    task = " ".join(ctx.args)
    print(task)
    log_command("software")
    update.message.reply_text("\n".join([row[0] for row in ss.sheet("sw").get_all_values()]))