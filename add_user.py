from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config

def add_user(bot, update):
    update.message.reply_text('Введите нового пользователя')

def add_new_user(bot, update, user_data):
    new_user = update.message.text
    print(update.message)
    user_data['teacher1'].append(new_user)


def main():
    mybot = Updater(config.API_KEY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("add", add_user, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, add_new_user, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
