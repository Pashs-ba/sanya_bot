
from utils import *

logging.basicConfig(filename='error.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.ERROR)
logging.basicConfig(filename='info.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)



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
        if not (message.from_user.username in get_user()):
            if message.from_user.username == 'r_comrad' or message.from_user.username == 'Pashs_ba':
                register(message.from_user.username, message.chat.id)
                bot.send_message(message.chat.id, 'Для пингакоманда /ping')
            else:
                register(message.from_user.username, message.chat.id)
                bot.send_message(message.chat.id, 'Бот Сани для пинга')
        else:
            bot.send_message(message.chat.id, 'Я жива!')
            for i in admin:
                bot.send_message(admin[i],
                                 '{} послал боту сообщение: {}, id {}'.format(message.from_user.username, message.text,
                                                                              message.chat.id))

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        logging.error("", exc_info=True)
