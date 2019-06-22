from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import config
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', #добавил логирование
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start(bot, update, user_data):
    update.message.reply_text('Введите преподавателя', reply_markup=ReplyKeyboardRemove())
    return 'teachers_group'


def find_teachers_group(bot, update, user_data):
    teachers_name = update.message.text
    print(teachers_name)
    with open('teacher1.txt', 'r', encoding='ptcp154') as t1_file: #Здесь будет проверка, есть ли такой преподаватель и список его учеников из бд
        user_data['teacher1'] = list(t1_file.read().split('\n'))
    my_keyboard = ReplyKeyboardMarkup([
        ['/list'],
        ['/edit_group'],
        ['/?']
    ])
    update.message.reply_text('Выберите действие', reply_markup=my_keyboard) #Без текстового сообщения клава почему-то не появляется
    return 'actions'


def edit_group(bot, update, user_data):
    return 'edit'

def ask_user_name(bot, update):
    update.message.reply_text('Введите нового пользователя')



def add_new_user(bot, update, user_data):
    #print(user_data['teacher1'])
    new_user = update.message.text
    user_data['teacher1'].append(new_user) #Добавляем нового ученика в user_data
    with open('teacher1.txt', 'a', encoding='ptcp154') as t1_file:  #Здесь мы будем добавлять нового ученика не в текстовый документ, а в бд
        t1_file.write(f'\n{new_user}')


def delete_user(bot, update, user_data): #создаю функцию удаления юзера
    del_user = update.message.text
    try:
        user_data['teacher1'].remove(del_user)
    except ValueError:
        update.message.reply_text('Нет такого студента')
    except TypeError:
        update.message.reply_text('')
    except KeyError:
        update.message.reply_text('Введите имя преподавателя')



def see_students_list(bot, update, user_data): # Просмотр всех учеников
    students_list = ''
    for student in user_data['teacher1']:
        students_list += f'{student}\n'
    update.message.reply_text(students_list)


def main():
    mybot = Updater(config.API_KEY, request_kwargs=config.PROXY)
    
    logging.info('Бот запускается')

    dialog = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        states = {
            'teachers_group': [MessageHandler(Filters.text, find_teachers_group, pass_user_data=True)],
            'actions': [CommandHandler('list', see_students_list, pass_user_data=True),
                        CommandHandler('edit_group', edit_group, pass_user_data=True)],
                        #CommandHandler('?', questions, pass_user_data=True)]
            'edit': [CommandHandler('add', ask_user_name),
                     MessageHandler(Filters.text, add_new_user, pass_user_data=True)]

        },
        fallbacks = []
    )

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("delete", delete_user, pass_user_data=True)) #добавил хендлер удаления

    dp.add_handler(dialog)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
