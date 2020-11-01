import configparser
import telebot
import logging


def create_bot() -> telebot.TeleBot:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    token = config['MAIN']['token']
    return telebot.TeleBot(token)


def enable_logging() -> None:
    logging.basicConfig(
        filename='error.log', filemode='a',
        format='%(asctime)s - %(message)s', level=logging.ERROR)
    logging.basicConfig(
        filename='info.log', filemode='a',
        format='%(asctime)s - %(message)s', level=logging.INFO)