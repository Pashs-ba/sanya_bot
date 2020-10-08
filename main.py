import telebot
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
token = config['MAIN']['token']

bot = telebot.TeleBot(token)


@bot.message_handler()
def main(message):
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