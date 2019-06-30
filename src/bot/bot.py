# -*- coding: utf-8 -*-

import telebot
import json

import sys
import logging

from telebot import TeleBot, apihelper, types
from db.mongo import connect
from config import token, proxy, db_url, db_collection
from utils.keyboard import create_menu

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

sys.path.append('../resources/')
from config import db_url, db_collection

apihelper.proxy = {'https': proxy}
bot = TeleBot(token)
telebot.logger.setLevel(logging.DEBUG)
# bot.enable_save_next_step_handlers(delay=2)

text_messages = {
    'start':
        u'Приветствую тебя, {name}!\n',
    'help':
        u'Пока что я не знаю, чем тебе помочь, поэтому просто выпей кофе!'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # markup.row('гитара', 'сейчас')
    markup.row('автор', 'сцена')

    msg = bot.send_message(message.from_user.id,
                           text_messages['start'].format(name=message.from_user.first_name),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, choose_category)


@bot.message_handler(content_type=['text'])
def choose_category(message):
    db = connect(db_url, db_collection)
    new_menu = []
    new_msg = ''
    new_handler = None

    if message.text == 'автор':
        new_menu = ['по алфавиту', 'по имени']
        new_msg = 'Как вы хотите выбрать?'
        new_handler = choose_author_l1

    elif message.text == 'сцена':
        for scene in db['scenes'].find():
            new_menu.append(scene['name'])
            new_msg = 'Выберите пожалуйста сцену'
            new_handler = choose_scene_l1

    markup = create_menu(new_menu, back=True)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)
    bot.register_next_step_handler(msg, new_handler)


@bot.message_handler(content_type=['text'])
def choose_scene_l1(message):
    """
    choose_scene_l1 -> (имя, дата) -> choose_scene_final
    """
    new_menu = ['Все дни', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    new_msg = 'Выберите пожалуйста день'

    if message.text == 'Назад':
        send_welcome(message)
        return

    markup = create_menu(new_menu, back=True)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)
    bot.register_next_step_handler(msg, choose_scene_final, message.text)


@bot.message_handler(content_type=['text'])
def choose_scene_final(message, name):
    db = connect(db_url, db_collection)

    if message.text == 'Назад':
        message.text = 'сцена'
        choose_category(message)
        return

    print("====")
    print(name)
    print(message.text)

    scene = db['scenes'].find({'name': name})[0]

    if message.text == 'Все дни':
        schedule = ''
        for day in ['Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
            schedule_day = scene[day]

            if schedule_day != '':
                schedule = schedule + '\n\n' + day + '\n' + schedule_day
        bot.send_message(message.from_user.id, schedule)
        bot.register_next_step_handler(message, choose_scene_final, name)
    elif message.text == 'Назад':
        bot.register_next_step_handler(message, send_welcome)
    else:
        print("====")
        print(message.text)

        if scene[message.text] != '':
            bot.send_message(message.from_user.id, scene[message.text])
        else:
            bot.send_message(message.from_user.id, 'В этот день ничего нет!')
        bot.register_next_step_handler(message, choose_scene_final, name)


@bot.message_handler(content_type=['text'])
def choose_author_l1(message):
    db = connect(db_url, db_collection)
    new_menu = []
    new_msg = ''
    new_handler = None

    if message.text == 'по алфавиту':
        for letter in db['letters'].find():
            new_menu.append(letter['name'])
        new_msg = "Выберите букву"
        new_handler = choose_author_l2
    elif message.text == 'по имени':
        pass

    markup = create_menu(new_menu, back=False)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)
    bot.register_next_step_handler(msg, new_handler)


def choose_author_l2(message):
    db = connect(db_url, db_collection)
    new_menu = []
    new_msg = 'sss'

    author_collection_name = db['letters'].find({'name': message.text})[0]['collection']

    for author in db[author_collection_name].find():
        new_menu.append(author['name'])

    markup = create_menu(new_menu, back=False)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)

    bot.register_next_step_handler(msg, choose_author_l3, author_collection_name)


def choose_author_l3(message, collection):
    db = connect(db_url, db_collection)

    new_menu = ['Все дни', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    new_msg = 'kek'
    new_handler = None

    markup = create_menu(new_menu, back=False)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)
    bot.register_next_step_handler(msg, choose_author_final, message.text)


@bot.message_handler(content_type=['text'])
def choose_author_final(message, name):
    db = connect(db_url, db_collection)

    if message.text == 'Все дни':
        pass
    else:
        schedule = db['authors'].find({'name': name})[0][message.text]

    bot.send_message(message.from_user.id, schedule)


def start_grushinka():
    try:
        bot.polling(none_stop=True)
    except BaseException as exception:
        print(exception)
        print('Connection refused')
