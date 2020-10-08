import telebot
import configparser
from random import randint

config = configparser.ConfigParser()
config.read('settings.ini')
token = config['MAIN']['token']

bot = telebot.TeleBot(token)
ans = {'Ня! Саня сказал, что тебя не было на занятиях, ууу, а если я разозлюсь?',
       'Эээ, а кодить? Вы и так вымираете, а ты не ходишь',
       'Эй! Ты чего меня обижаешь? Почему тебя не наблюдалось занятии?',
       'Здрасте, а чего это мы не кодим? Я ведь знаю, что тебя не было! Я всё знаю!'}
@bot.message_handler()
def main(message):
    admin = {'ivan2832': 1061564807,
             'Pashs_ba': 370666658}
    if message.from_user.username in admin:
        bot.send_message(message.chat.id, 'Будущая админка')
        print(message.chat.id, message.from_user.username)
    else:
        bot.send_message(message.chat.id, ans[randint(0, len(ans) - 1)])
    for i in admin:
        bot.send_message(admin[i], '{} послал боту такое сообщение: {}, id {}'.format(message.from_user.username, message.text, message.chat.id))


if __name__ == '__main__':
    bot.polling(none_stop=True)