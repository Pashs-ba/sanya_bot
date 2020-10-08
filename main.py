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
    print(r.split())


@bot.message_handler(commands=['ping'])
def ping(message):
    global IS_PING
    print('sd')
    if message.from_user.username == 'Pashs_ba':
        IS_PING = True
        bot.send_message(message.chat.id, 'Введи ники неугодных одним сообщением, разделяя их пробелом')
    else:
        bot.send_message(message.chat.id, 'Пшел кодить')


@bot.message_handler()
def main(message):
    global IS_PING
    if IS_PING and message.from_user.username == 'Pashs_ba':
        slaves = message.text.split()
        for i in slaves:
            i = i[1:]
        print(slaves)
        IS_PING = False
    else:
        admin = {'ivan2832': 1061564807,
                 'Pashs_ba': 370666658}
        if message.from_user.username in admin:
            bot.send_message(message.chat.id, 'Будущая админка')
            print(message.chat.id, message.from_user.username)
        else:
            bot.send_message(message.chat.id, 'Пшел кодить')
        for i in admin:
            bot.send_message(admin[i], '{} послал боту такое сообщение: {}, id {}'.format(message.from_user.username, message.text, message.chat.id))





if __name__ == '__main__':
    bot.polling(none_stop=True)