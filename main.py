
from utils import *

logging.basicConfig(filename='error.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.ERROR)
logging.basicConfig(filename='info.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

ans = ['Слушай, дай отдохнуть',
       'Ня, ну вот почему вы все такие злые? Я сижу, отдыхаю от Саниных запросов, а ты меня донимаешь',
       'Если ты думаешь, что боты не имеют права посидеть в тишине, то ты сильно ошибаешься',
       'Слушай, я на работе, мне не до болтавни, поговорим тогда, когда ты посмеешь прогулять занятие']


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
    global IS_PING, admin, ans
    if IS_PING and message.from_user.username in admin:
        send_message(message)
        IS_PING = False
    else:
        if not (message.from_user.username in get_user()):
            if message.from_user.username == 'r_comrad' or message.from_user.username == 'Pashs_ba':
                register(message.from_user.username, message.chat.id)
                bot.send_message(message.chat.id, 'Для пинга команда /ping')
            else:
                register(message.from_user.username, message.chat.id)
                bot.send_message(message.chat.id, 'Бот Сани для пинга')
        else:
            bot.send_message(message.chat.id, ans[random.randint(0, len(ans)-1)])
            for i in admin:
                bot.send_message(admin[i],
                                 '{} послал боту сообщение: {}, id {}'.format(message.from_user.username, message.text,
                                                                              message.chat.id))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        logging.error("", exc_info=True)
