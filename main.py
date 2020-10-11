from utils import *

logging.basicConfig(filename='error.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.ERROR)
logging.basicConfig(filename='info.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

proud = ['Слушай, дай отдохнуть',
         'Ня, ну вот почему вы все такие злые? Я сижу, отдыхаю от Саниных запросов, а ты меня донимаешь',
         'Если ты думаешь, что боты не имеют права посидеть в тишине, то ты сильно ошибаешься',
         'Слушай, я на работе, мне не до болтавни, поговорим тогда, когда ты посмеешь прогулять занятие']


@bot.message_handler(commands=['ping'])
def ping(message):
    global IS_PING, admin
    if message.from_user.username in admin:
        IS_PING = True
        bot.send_warning(message.chat.id, 'Введи ники неугодных одним сообщением, разделяя их пробелом')
    else:
        bot.send_warning(message.chat.id, 'Пшёл кодить')


@bot.message_handler(commands=['global_message'])
def global_message(message):
    global IS_MESSAGE, admin
    if message.from_user.username in admin:
        IS_MESSAGE = True
        bot.send_message(message.chat.id, 'Напиши сообщения для всех людей')


@bot.message_handler()
def main(message):
    global IS_PING, IS_MESSAGE, admin, proud
    if IS_PING and message.from_user.username in admin:
        send_warning(message)
        IS_PING = False
    elif IS_MESSAGE and message.from_user.username in admin:
        send_global_message(message)
        IS_MESSAGE = False
    else:
        if not (message.from_user.username in get_user()):
            if message.from_user.username == 'r_comrad' or message.from_user.username == 'Pashs_ba':
                register(message.from_user.username, message.chat.id)
                bot.send_warning(message.chat.id, 'Для пинга команда /ping')
            else:
                register(message.from_user.username, message.chat.id)
                bot.send_warning(message.chat.id, 'Бот Сани для пинга')
        else:
            bot.send_warning(message.chat.id, proud[random.randint(0, len(proud) - 1)])
            for i in admin:
                bot.send_warning(admin[i],
                                 '{} послал боту сообщение: {}, id {}'.format(message.from_user.username, message.text,
                                                                              message.chat.id))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        logging.error("", exc_info=True)
