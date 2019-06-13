from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config

def add_user(bot, update):
    update.message.reply_text('Введите нового пользователя') 
    #Нельзя ли эту функцию использовать и для введения ника удаляемого юзера?Это же возможно?)
    #К примеру обозвать просто 'Введите username пользователя'

def add_new_user(bot, update, user_data):
    new_user = update.message.text
    print(update.message)
    user_data['teacher1'].append(new_user)

def delete_user(bot, update, user_data): #создаю функцию
    del_user = update.message.text       #передаю в переменную значение (юзер который удалить)
    print(update.message)
    user_data[''].remove(del_user)       #тут мне нужно объяснить, как написать, 
                                         #чтоб он понял какой именно удалить элемент


def main():
    mybot = Updater(config.API_KEY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("add", add_user, pass_user_data=True))
    dp.add_handler(CommandHandler("delete", delete_user, pass_user_data=True)) #добавил хендлер удаления

    dp.add_handler(MessageHandler(Filters.text, add_new_user, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
