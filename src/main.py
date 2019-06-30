# -*- coding: utf-8 -*-

import telebot
import sys
import os
import logging
import json

#from multiprocessing import Process
from threading import Thread

from telebot import TeleBot, apihelper, types

from db.mongo import connect

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))

from config import token, proxy, db_url, db_collection
from functions import get_letters, callback_authors_by_letter, callback_author_time, callback_author_time_2
from utils.updater import update_scenes, update_authors

apihelper.proxy = {'https': proxy}
bot = TeleBot(token)
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['now'])
def now(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Сейчас на фестивале', url='https://scn.grushinka.ru/now')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на сайт.", reply_markup=markup)


@bot.message_handler(commands=['сцена'])
def scene(message):
    pass


@bot.message_handler(commands=['буква'])
def letter(message):
    keyboard = types.InlineKeyboardMarkup()

    row = []
    for letter in get_letters():
        row.append(types.InlineKeyboardButton(letter, callback_data=json.dumps({'letter': letter})))

    keyboard.row(*row)

    bot.send_message(message.chat.id, 'Выберите букву:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    try:
        data = json.loads(query.data)
        if 'letter' in data:
            callback_authors_by_letter(bot, query, data['letter'])

        elif 'author' in data:
            callback_author_time(bot, query, data['author'])

        elif 'author_url' in data:
            print('WE HERE')
            callback_author_time_2(bot, query, data['author_url'])



    except ValueError:
        pass


if __name__ == '__main__':



    #Process(target=update_scenes, args=()).start()
    update_authors_proccess = Thread(target=update_scenes, args=())
    update_authors_proccess.start()
    update_authors_proccess.join()

    try:
        pass
        # bot.polling(none_stop=True)
    except BaseException as exception:
        print(exception)
        print('Connection refused')
