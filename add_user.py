from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import config
import logging


import db_users as db
from handlers import *
from db_users import Users
from create_user import add_new_user

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', #добавил логирование
                    level=logging.INFO,
                    filemode='w',
                    filename='bot.log'
                    )

def main():

    mybot = Updater(config.API_KEY, request_kwargs=config.PROXY)
    
    logging.info('Бот запускается')

    data_user_dialog = ConversationHandler(
        entry_points=[CommandHandler('add', data_user_dialog_start, pass_user_data=True)],
        states={
            'user':[MessageHandler(Filters.text, data_user_dialog_user, pass_user_data=True)],
            'github':[MessageHandler(Filters.text, data_user_dialog_git, pass_user_data=True)],
            'gmt':[MessageHandler(Filters.text, data_user_dialog_gmt, pass_user_data=True)],
            'save_to_db':[MessageHandler(Filters.text, save_data_users, pass_user_data=True)],
                          
        },
        fallbacks=[MessageHandler(Filters, get_fallback, pass_user_data=True)]
    )

    main_dialog = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        states={
            'teachers_group': [MessageHandler(Filters.text, find_teachers_group, pass_user_data=True)],
            'actions': [CommandHandler('list', see_students_list, pass_user_data=True),
                        CommandHandler('edit_group', edit_group, pass_user_data=True)],
                        # CommandHandler('questions', show_questions, pass_user_data=True)]
            'edit': [data_user_dialog,
                     CommandHandler('back', back_edit, pass_user_data=True),
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

    dp.add_handler(main_dialog)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
