from config import bot, ss

def log_command(cmd: str): print(f"[!!] Command {cmd} called")

@bot.message_handler(commands=["getinfo"])
def getinfo(message):
    log_command("getinfo")
    bot.reply_to(message, str(ss.sheet("hw").get_all_values()))


@bot.message_handler(commands=["software", "sw"])
def sw(message):
    log_command("software")
    bot.reply_to(message, "\n".join([row[0] for row in ss.sheet("sw").get_all_values()]))