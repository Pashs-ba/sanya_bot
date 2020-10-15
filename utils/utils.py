import logging
import random
import telebot
import configparser
import pickle
from utils.users import *

ans = ['Ня! Саня сказал, что тебя не было на занятиях, ууу, а если я разозлюсь?',
       'Эээ, а кодить? Вы и так вымираете, а ты не ходишь',
       'Эй! Ты чего меня обижаешь? Почему тебя не наблюдалось на занятии?',
       'Здрасте, а чего это мы не кодим? Я ведь знаю, что тебя не было! Я всё знаю!']


config = configparser.ConfigParser()
config.read('settings.ini')
token = config['MAIN']['token']
bot = telebot.TeleBot(token)

IS_PING = False
IS_MESSAGE = False


def get_user() -> dict:
    with open('data.pickle', 'rb') as f:
        ret = pickle.load(f)
    return ret


def load_data(data):
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)


def register(id: int, name, surname, nickname):
    data = get_user()
    data['students'].append(Student(id, name, surname, nickname))
    load_data(data)


def send_warning(message):
    try:
        global ans
        slaves = message.text.split()
        new_slaves = []
        for i in slaves:
            if i[0] == '@':
                new_slaves.append(i[1:])
            else:
                new_slaves.append(i)
        resisted = get_user()
        print(new_slaves)
        for i in new_slaves:
            is_been = False
            for j in resisted['students']:
                if i == j.nickname:
                    logging.info(ans[random.randint(0, len(ans) - 1)])
                    bot.send_message(j.id, ans[random.randint(0, len(ans) - 1)])
                    is_been = True
            if not is_been:
                bot.send_message(message.chat.id, '{} не нашла в списке зареганных'.format(i))
    except:
        logging.error("Exception occurred", exc_info=True)


def send_global_message(message):
    users = get_user()
    for i in users['students']:
        bot.send_message(i.id, 'Сообщение от Сани: '+message.text)


def is_in_admins(nickname):
    users = get_user()
    a = False
    for i in users['admins']:
        if i.nickname == nickname:
            a = True
    return a


if __name__ == '__main__':
    print(get_user())
