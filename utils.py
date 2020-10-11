import logging
import random
import telebot
import configparser


ans = ['Ня! Саня сказал, что тебя не было на занятиях, ууу, а если я разозлюсь?',
       'Эээ, а кодить? Вы и так вымираете, а ты не ходишь',
       'Эй! Ты чего меня обижаешь? Почему тебя не наблюдалось на занятии?',
       'Здрасте, а чего это мы не кодим? Я ведь знаю, что тебя не было! Я всё знаю!']
admin = {'ivan2832': 1061564807,
         'Pashs_ba': 370666658, }


config = configparser.ConfigParser()
config.read('settings.ini')
token = config['MAIN']['token']
bot = telebot.TeleBot(token)

IS_PING = False


def get_user():
    with open('users.txt', 'r') as f:
        r = f.read()
    s = r.split(';')
    ret = {}
    for i in s:
        tmp = i.split()
        if tmp:
            ret.update({tmp[0]: int(tmp[1])})
    return ret


def register(username, id):
    with open('users.txt', 'a') as f:
        f.write('{} {};'.format(username, id))


def send_message(message):
    try:
        global ans
        slaves = message.text.split()
        new_slaves = []
        for i in slaves:
            if i[1] == '@':
                new_slaves.append(i[1:])
            else:
                new_slaves.append(i)
        register = get_user()
        for i in new_slaves:
            if i in register:
                logging.info(ans[random.randint(0, len(ans) - 1)])
                bot.send_message(register[i], ans[random.randint(0, len(ans) - 1)])
            else:
                bot.send_message(message.chat.id, '{} не нашла в списке зареганных'.format(i))
    except:
        logging.error("Exception occurred", exc_info=True)
