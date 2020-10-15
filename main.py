from utils.utils import *


logging.basicConfig(filename='log/error.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.ERROR)
logging.basicConfig(filename='log/info.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

proud = ['Слушай, дай отдохнуть',
         'Ня, ну вот почему вы все такие злые? Я сижу, отдыхаю от Саниных запросов, а ты меня донимаешь',
         'Если ты думаешь, что боты не имеют права посидеть в тишине, то ты сильно ошибаешься',
         'Слушай, я на работе, мне не до болтавни, поговорим тогда, когда ты посмеешь прогулять занятие']


@bot.message_handler(commands=['ping'])
def ping(message):
    global IS_PING
    if is_in_admins(message.from_user.username):
        IS_PING = True
        bot.send_message(message.chat.id, 'Введи ники неугодных одним сообщением, разделяя их пробелом')
    else:
        bot.send_message(message.chat.id, 'Пшёл кодить')


@bot.message_handler(commands=['global_message'])
def global_message(message):
    global IS_MESSAGE
    if is_in_admins(message.from_user.username):
        IS_MESSAGE = True
        bot.send_message(message.chat.id, 'Напиши сообщения для всех людей')


@bot.message_handler()
def main(message):
    global IS_PING, IS_MESSAGE, admin, proud
    if IS_PING and is_in_admins(message.from_user.username):
        send_warning(message)
        IS_PING = False
    elif IS_MESSAGE and is_in_admins(message.from_user.username):
        send_global_message(message)
        IS_MESSAGE = False
    else:
        users = get_user()
        a = 1
        for i in users['students']:
            if i.nickname == message.from_user.username:
                a = 0
        if a:
            if message.from_user.username == 'r_comrad' or message.from_user.username == 'Pashs_ba':
                register(message.chat.id, message.from_user.name, message.from_user.surname, message.from_user.username)
                bot.send_message(message.chat.id, 'Для пинга команда /ping')
            else:
                register(message.chat.id, message.from_user.name, message.from_user.surname, message.from_user.username)
                bot.send_message(message.chat.id, 'Бот Сани для пинга')
        else:
            bot.send_message(message.chat.id, proud[random.randint(0, len(proud) - 1)])
            admin = users['admins']
            for i in admin:
                bot.send_message(i.id,
                                 '{} послал боту сообщение: {}, id {}'.format(message.from_user.username, message.text,
                                                                              message.chat.id))


def from_txt_to_object():
    admin = {'ivan2832': 1061564807,
             'Pashs_ba': 370666658, }
    with open('users.txt', 'r') as f:
        r = f.read()
    s = r.split(';')
    ret = {}
    for i in s:
        tmp = i.split()
        if tmp:
            ret.update({tmp[0]: int(tmp[1])})
    data = {}
    students = []
    for i in ret:
        students.append(Student(ret[i], None, None, i))
    ad = []
    for i in admin:
        ad.append(Admin(ret[i], None, None, i))
    data.update({'admins': ad,
                 'students': students})
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        logging.error("", exc_info=True)

    # from_txt_to_object()
    # print(get_user())
