from config import bot, ss

@bot.message_handler(commands=["ss"])
def ss(message):
    bot.send_message(message, ss.get_all_cells())