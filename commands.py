from config import bot, ss

def log_command(cmd: str): print(f"[!!] Command {cmd} called")

@bot.message_handler(commands=["getinfo"])
def getinfo(message):
    log_command("getinfo")
    bot.reply_to(message, ss.sheet("sw").get_all_cells())