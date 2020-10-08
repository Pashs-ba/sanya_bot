import telebot
import configparser

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


@bot.message_handler(commands=['ping'])
def ping(message):
    global IS_PING

    if message.from_user.username == 'Pashs_ba':
        IS_PING = True
        bot.send_message(message.chat.id, 'Введи ники неугодных одним сообщением, разделяя их пробелом')
    else:
        bot.send_message(message.chat.id, 'Пшел кодить')


def send_message(message):
    slaves = message.text.split()
    new_slaves = []
    for i in slaves:
        new_slaves.append(i[1:])
    bot.send_message(message.chat.id, 'Приступил к работе')
    register = get_user()
    for i in new_slaves:
        if i in register:
            bot.send_message(register[i], 'Гда ты?')



@bot.message_handler()
def main(message):
    global IS_PING
    if IS_PING and message.from_user.username == 'Pashs_ba':
        send_message(message)
        IS_PING = False
    else:
        # 'ivan2832': 1061564807,
        admin = {
                 'Pashs_ba': 370666658}
        get_user()
        if message.from_user.username in admin:
            bot.send_message(message.chat.id, 'Будущая админка')
            print(message.chat.id, message.from_user.username)
        else:
            bot.send_message(message.chat.id, 'Пшел кодить')
        for i in admin:
            bot.send_message(admin[i], '{} послал боту такое сообщение: {}, id {}'.format(message.from_user.username, message.text, message.chat.id))


if __name__ == '__main__':
    bot.polling(none_stop=True)