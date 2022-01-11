from config import bot, ss


print("[!] Bot loaded")
bot.polling()
# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as e:
#         print(e)
#         time.sleep(5)


if __name__ == "__main__":
    bot.polling()