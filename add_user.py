from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import config
import logging

import db_users as db
from db_users import Users
from create_user import add_new_user

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', #добавил логирование
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start(bot, update, user_data):
    update.message.reply_text('Введите преподавателя', reply_markup=ReplyKeyboardRemove())#предлагаю Введите преподавателя убрать и сделать кнопку выберите преподавателя, нажимая будет выпадать список
    return 'teachers_group'


def find_teachers_group(bot, update, user_data):
    teachers_name = update.message.text
    print(teachers_name)
    with open('teacher1.txt', 'r', encoding='ptcp154') as t1_file:
        # TODO: Здесь будет проверка, есть ли такой преподаватель и список его учеников из бд
        user_data['teacher1'] = list(t1_file.read().split('\n'))
    my_keyboard = ReplyKeyboardMarkup([
        ['/list'],
        ['/edit_group'],
        ['/questions']
    ])
    update.message.reply_text('Выберите действие', reply_markup=my_keyboard)
    return 'actions'


def edit_group(bot, update, user_data):
    students_list = ''
    for student in user_data['teacher1']:
        students_list += f'{student}\n'
    my_keyboard = ReplyKeyboardMarkup([
        ['/add'],
        ['/delete']
        # ['/back']
    ])
    update.message.reply_text(students_list, reply_markup=my_keyboard)
    return 'edit'


def ask_user_name(bot, update):
    update.message.reply_text('Введите нового пользователя', reply_markup=ReplyKeyboardRemove())


#  def add_new_user(bot, update, user_data):
#    """Запись информации о пользователе в текстовый файл"""
#    new_user = update.message.text
#    user_data['teacher1'].append(new_user)  # Добавляем нового ученика в user_data
#    with open('teacher1.txt', 'a', encoding='ptcp154') as t1_file:
#        # TODO: Здесь мы будем добавлять нового ученика не в текстовый документ, а в бд
#        t1_file.write(f'\n{new_user}')


def delete_user(bot, update, user_data):  # создаю функцию удаления юзера
    del_user = update.message.text
    try:
        user_data['teacher1'].remove(del_user)
    except ValueError:
        update.message.reply_text('Нет такого студента')
    except TypeError:
        update.message.reply_text('')
    except KeyError:
        update.message.reply_text('Введите имя преподавателя')


def see_students_list(bot, update, user_data):  # Просмотр всех учеников
    students_list_keyboard = []
    for student in user_data['teacher1']:
        student_button = list[student]
        students_list_keyboard.append(student_button)
    update.message.reply_text('Список студентов:', students_list_keyboard)
    return 'student'


def see_students_tasks(bot, update, user_data):
    students_name = update.message.text()
    tasks_keyboard = [
        ['/done_tasks'],
        ['/undone_tasks'],
        ['/questions']
    ]
    update.message.reply_text('', tasks_keyboard)
    return 'tasks'


def get_fallback(bot, update, user_data):
    update.message.reply_text('Пожалуйста, переформулируйте ответ')

def save_users(user='Sergey', git_url='www.github.com', gmt=2):
    #try:
    repeat_user = Users.query.filter(Users.user == user).order_by(Users.gmt, git_url).first()
    print(repeat_user)
    if not repeat_user:   
        new_user = Users(user=user, git_url=git_url, gmt=gmt)
        db.db_session.add(new_user)
        db.db_session.commit()
    #except:
        #update.message.reply_text('')


def main():
    save_users()

    mybot = Updater(config.API_KEY, request_kwargs=config.PROXY)
    
    logging.info('Бот запускается')

    dialog = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        states={
            'teachers_group': [MessageHandler(Filters.text, find_teachers_group, pass_user_data=True)],
            'actions': [CommandHandler('list', see_students_list, pass_user_data=True),
                        CommandHandler('edit_group', edit_group, pass_user_data=True)],
                        # CommandHandler('questions', show_questions, pass_user_data=True)]
            'edit': [CommandHandler('add', ask_user_name),
                     CommandHandler('delete', delete_user, pass_user_data=True),
                     MessageHandler(Filters.text, add_new_user, pass_user_data=True)],
            'student': [MessageHandler(Filters.text, see_students_tasks, pass_user_data=True)]
            #'tasks': [CommandHandler('done_tasks', show_done_tasks, pass_user_data=True),
                     # CommandHandler('undone_tasks', show_undone_tasks, pass_user_data=True),
                    # CommandHandler('questions', show_questions, pass_user_data=True),]

        },
        fallbacks=[MessageHandler(Filters, get_fallback, pass_user_data=True)]
    )

    dp = mybot.dispatcher

    dp.add_handler(dialog)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
