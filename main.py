from bot import bot

if __name__ == "__main__":
    print("[!] Bot started")

    # Starts bot
    bot.start_polling()
    bot.idle()
    