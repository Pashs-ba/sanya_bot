import telebot
import configparser
import random
config = configparser.ConfigParser()
config.read('settings.ini')
token = config['MAIN']['token']

bot = telebot.TeleBot(token)
IS_PING = False
ans = ['Ня! Саня сказал, что тебя не было на занятиях, ууу, а если я разозлюсь?',
       'Эээ, а кодить? Вы и так вымираете, а ты не ходишь',
       'Эй! Ты чего меня обижаешь? Почему тебя не наблюдалось на занятии?',
       'Здрасте, а чего это мы не кодим? Я ведь знаю, что тебя не было! Я всё знаю!']
admin = {'ivan2832': 1061564807,
         'Pashs_ba': 370666658,
         'r_comrad': 239460102}

def get_user():
    with open('users.txt', 'r') as f:
        r = f.read(),
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


@bot.message_handler(commands=['ping'])
def ping(message):
    global IS_PING, admin

    if message.from_user.username in admin:
        IS_PING = True
        bot.send_message(message.chat.id, 'Введи ники неугодных одним сообщением, разделяя их пробелом')
    else:
        bot.send_message(message.chat.id, 'Пшёл кодить')





@bot.message_handler()
def main(message):

    global IS_PING, admin
    if IS_PING and message.from_user.username in admin:
        send_message(message)
        IS_PING = False
    else:
        if not(message.from_user.username in get_user()):
            if message.from_user.username == 'r_comrad' or message.from_user.username == 'Pashs_ba':
                register(message.from_user.username, message.chat.id)
                bot.send_message(message.chat.id, 'Для пинга команда /ping')
            else:
                register(message.from_user.username, message.chat.id)
                bot.send_message(message.chat.id, 'Бот Сани для пинга')
        else:
            bot.send_message(message.chat.id, 'Я жива!')
            for i in admin:
                bot.send_message(admin[i], '{} послал боту сообщение: {}, id {}'.format(message.from_user.username, message.text, message.chat.id))


def send_message(message):
    try:
        global ans
        slaves = message.text.split()
        new_slaves = []
        for i in slaves:
            new_slaves.append(i[1:])
        register = get_user()
        for i in new_slaves:
            if i in register:
                bot.send_message(register[i], ans[random.randint(0, len(ans)-1)])
    except:
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True)