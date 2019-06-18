from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', #добавил логирование
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start(bot, update, user_data): #Добавила команду старт. На ней будет открываться файл со списком учеников и записываться в user_data
    with open('teacher1.txt', 'r', encoding='ptcp154') as t1_file:
        user_data['teacher1'] = list(t1_file.read().split('\n'))

def add_user(bot, update):
    update.message.reply_text('Введите нового пользователя') 


def add_new_user(bot, update, user_data):
    #print(user_data['teacher1'])
    new_user = update.message.text
    user_data['teacher1'].append(new_user) #Добавляем нового ученика в user_data
    with open('teacher1.txt', 'a', encoding='ptcp154') as t1_file:  # и в список учеников, чтобы при следующем запуске бота новый ученик не потерялся
        t1_file.write(f'\n{new_user}')
    #print(user_data['teacher1'])

def delete_user(bot, update, user_data): #создаю функцию удаления юзера
    del_user = update.message.text
    try:
        user_data['teacher1'].remove(del_user)
    except ValueError:
        update.message.reply_text('Нет такого студента')
    #except TypeError:
    #    update.message.reply_text('')
    except KeyError:
        update.message.reply_text('Введите имя преподавателя')



def see_students_list(bot, update, user_data): # Просмотр всех учеников
    students_list = ''
    for student in user_data['teacher1']:
        students_list += f'{student}\n'
     #    print(students_list)
    # print(students_list)
    update.message.reply_text(students_list)


def main():
    mybot = Updater(config.API_KEY, request_kwargs=config.PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('add', add_user))
    dp.add_handler(CommandHandler('list', see_students_list, pass_user_data=True))
    dp.add_handler(CommandHandler("delete", delete_user, pass_user_data=True)) #добавил хендлер удаления

    dp.add_handler(MessageHandler(Filters.text, add_new_user, pass_user_data=True))



    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
