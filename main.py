import telebot
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
token = config['MAIN']['token']

bot = telebot.TeleBot(token)


@bot.message_handler()
def handle_start_help(message):

    admin = {'ivan2832': 0,
             'Pashs_ba': 370666658}
    if message.from_user.username in admin:
        bot.send_message(message.chat.id, 'Будущая админка')
        print(message.chat.id, message.from_user.username)
    else:
        bot.send_message(message.chat.id, 'Не для тебя холоп')


if __name__ == '__main__':
    bot.polling(none_stop=True)