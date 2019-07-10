from model import Student, db_session


def add_new_user(bot, update, user_data):
    new_user = update.message.text
    # TODO: Проверка, что такого пользователя нет
    new_student = Student(username=new_user, role='student')
    user_data['teacher1'].append(new_user)  # Добавляем нового ученика в user_data
    db_session.add(new_user)  # Добавляем студента в базу

