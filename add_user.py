from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', #добавил логирование
                    level=logging.INFO,
                    filename='bot.log'
                    )


def add_user(bot, update):
    update.message.reply_text('Введите нового пользователя') 


def add_new_user(bot, update, user_data):
    new_user = update.message.text
    print(update.message)
    user_data['teacher1'].append(new_user)

def delete_user(bot, update, user_data): #создаю функцию удаления юзера
    print('!')
    del_user = update.message.text       
    print(update.message)
    try:
        user_data['teacher1'].remove(del_user)
    except ValueError:
        update.message.reply_text('Нет такого студента') 
                                      

def main():
    mybot = Updater(config.API_KEY, request_kwargs=config.PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("add", add_user, pass_user_data=True))
    dp.add_handler(CommandHandler("delete", delete_user, pass_user_data=True)) #добавил хендлер удаления

    dp.add_handler(MessageHandler(Filters.text, add_new_user, pass_user_data=True))



    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
