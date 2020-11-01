import logging
import peewee
import models
import json
import utils
import os
import telebot
import configparser


DEBUG = False if os.environ.get("DEBUG", False) else True
if DEBUG:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    TOKEN = config['MAIN']['token']
else:
    TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)


utils.enable_logging()
db = peewee.SqliteDatabase('data.db')
with open("phrases.json", "r") as f:
    MSG = json.load(f)


def createTables():
    with db:
        db.create_tables([models.Users])


def getCurrentUser(message):
    return models.Users.get_or_none(
        models.Users.id == message.from_user.id
    )


def initialize_admins():
    admins_ids = [401602836]
    for id in admins_ids:
        user = models.Users.get_or_none(id=id)
        if user is not None:
            user.is_admin = True
            user.save()


def admin_only(func):
    def wrapper(message):
        user = getCurrentUser(message)
        if user is not None and user.is_admin:
            func(message)
        else:
            bot.send_message(message.chat.id, MSG['ADMIN_ONLY'])
    return wrapper


@bot.message_handler(commands=["admin"])
@admin_only
def admin(message):
    bot.send_message(message.chat.id, MSG['ADMIN_GREETING'])


def sendToEveryStudent(text):
    students = models.Users.select().where(models.Users.is_teacher == False)
    for student in students:
        bot.send_message(student.chat_id, MSG['PING_RECIEVED'])
        bot.send_message(student.chat_id, text)


@admin_only
def pingStudentsInput(message):
    try:
        text = message.text
        sendToEveryStudent(text)
    except Exception as e:
        bot.send_message(message.chat.id, MSG['INVALID_INPUT'])
        print(e)


@bot.message_handler(commands=["ping"])
@admin_only
def pingStudents(message):
    bot.send_message(message.chat.id, MSG["SEND_PING"])
    bot.register_next_step_handler(message, pingStudentsInput)


@bot.message_handler(commands=['listAdmins'])
@admin_only
def listAdmins(message):
    adminList = models.Users.select().where(models.Users.is_admin)
    msg = (
        "Администраторы:\n" +
        '\n'.join(
            ' '.join((i.name, i.surname)) +
            " (" + str(i.id) + ")" for i in adminList)
    ) if adminList else "Администраторов пока что нет!"
    bot.send_message(message.chat.id, msg)


@admin_only
def addAdminInput(message):
    try:
        uid = int(message.text)
        user = models.Users.get_or_none(models.Users.id == uid)
        if user is not None:
            user.is_admin = True
            user.save()
            bot.send_message(message.chat.id, MSG["ADD_ADMIN_SUCCESS"])
        else:
            bot.send_message(message.chat.id, MSG["ADD_ADMIN_ERROR"])
    except Exception:
        bot.send_message(message.chat.id, MSG['INVALID_INPUT'])


@bot.message_handler(commands=['addAdmin'])
@admin_only
def addAdmin(message):
    bot.send_message(message.chat.id, MSG["ADD_ADMIN"])
    bot.register_next_step_handler(message, addAdminInput)


@admin_only
def delAdminInput(message):
    try:
        uid = int(message.text)
        user = models.Users.get_or_none(models.Users.id == uid)
        if user is not None:
            user.is_admin = False
            user.save()
            bot.send_message(message.chat.id, MSG["DEL_ADMIN_SUCCESS"])
        else:
            bot.send_message(message.chat.id, MSG["DEL_ADMIN_ERROR"])
    except Exception:
        bot.send_message(message.chat.id, MSG['INVALID_INPUT'])


@bot.message_handler(commands=['delAdmin'])
@admin_only
def delAdmin(message):
    bot.send_message(message.chat.id, MSG["DEL_ADMIN"])
    bot.register_next_step_handler(message, delAdminInput)


def registerUser(message):
    try:
        name, surname = message.text.split()
        models.Users.create(
            id=message.from_user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            name=name, surname=surname
        )
        bot.send_message(message.chat.id, MSG['REGISTER_SUCCESS'])
    except Exception:
        bot.reply_to(message, MSG['INVALID_INPUT'])


def registerYesNoAnswer(message):
    if message.text.lower() == "y":
        bot.send_message(message.chat.id, MSG['START_REGISTER'])
        bot.register_next_step_handler(message, registerUser)
    else:
        bot.send_message(message.chat.id, MSG['GOT_REJECTED'])


@bot.message_handler(commands=['help', 'start'])
def help(message):
    bot.send_message(message.chat.id, MSG['HELP'])


@bot.message_handler(commands=['listStudents'])
@admin_only
def listStudents(message):
    users = models.Users.select().where(models.Users.is_teacher == False)
    msg = "Id: {}\nНик: {}\nИмя: {}\nФамилия: {}\n\n"
    if not users:
        bot.send_message(message.chat.id, MSG['NO_STUDENTS'])
        return
    bot.send_message(message.chat.id, MSG['STUDENTSLIST'])
    text = ""
    for u in users:
        text += msg.format(u.id, u.username, u.name, u.surname)
        if len(text) > 3500:
            bot.send_message(message.chat.id, text)
            text = ""
    if text:
        bot.send_message(message.chat.id, text)


@bot.message_handler()
def main(message):
    user = getCurrentUser(message)
    if user is None:
        msg = bot.send_message(message.chat.id, MSG['NEED_TO_REGISTER'])
        bot.register_next_step_handler(msg, registerYesNoAnswer)
    else:
        bot.send_message(message.chat.id, MSG['KNOWN_USER'])


if __name__ == '__main__':
    try:
        with db:
            createTables()
            initialize_admins()
            bot.polling(none_stop=True)
    except Exception:
        logging.error("", exc_info=True)
