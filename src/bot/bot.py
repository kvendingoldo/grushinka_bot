# -*- coding: utf-8 -*-

import telebot
import json
import sys
import logging

from telebot import TeleBot, apihelper, types

from db.mongo import connect
from config import token, proxy, db_url, db_collection
from utils.keyboard import create_menu

sys.path.append('../resources/')
from config import db_url, db_collection

apihelper.proxy = {'https': proxy}
bot = TeleBot(token)
telebot.logger.setLevel(logging.INFO)
# bot.enable_save_next_step_handlers(delay=2)

text_messages = {
    'start':
        u'Приветствую тебя, {name}!\nВ случае проблем с ботом официальный сайт с расписанием доступен тут: https://scn.grushinka.ru',
    'help':
        'Доступные команды:\n/site - официальный сайт\n/help - подсказка\n/start - начать работу с ботом',
    'site':
        'Сайт с официальным расписанием доступен тут: https://scn.grushinka.ru'
}


@bot.message_handler(commands=['site'])
def send_help(message):
    bot.send_message(message.from_user.id, text_messages['site'])


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, text_messages['help'])


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
        new_menu = ['по алфавиту']  # , 'по имени']
        new_msg = 'Выберите пожалуйста букву'
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

    scene = db['scenes'].find({'name': name})[0]

    if message.text == 'Все дни':
        schedule = ''
        for day in ['Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
            if day in scene:
                schedule_day = scene[day]

                if (schedule_day != '') and (schedule_day is not None):
                    schedule = schedule + '\n\n' + day + '\n' + schedule_day
        if schedule != '':
            bot.send_message(message.from_user.id, schedule)
        else:
            bot.send_message(message.from_user.id, 'Ничего нет!')
        bot.register_next_step_handler(message, choose_scene_final, name)

    else:
        if message.text in scene:
            if scene[message.text] != '':
                bot.send_message(message.from_user.id, scene[message.text])
            else:
                bot.send_message(message.from_user.id, 'В этот день ничего нет!')
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
    # elif message.text == 'по имени':
    #    pass
    elif message.text == 'Назад':
        send_welcome(message)
        return

    markup = create_menu(new_menu, back=True)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)
    bot.register_next_step_handler(msg, new_handler)


def choose_author_l2(message):
    db = connect(db_url, db_collection)
    new_menu = []
    new_msg = 'Выберите пожалуйста автора'

    if message.text == 'Назад':
        message.text = 'автор'
        choose_category(message)
        return

    author_collection_name = db['letters'].find({'name': message.text})[0]['collection']

    for author in db[author_collection_name].find():
        print(author)
        new_menu.append(author['name'])

    markup = create_menu(new_menu, back=True)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)

    bot.register_next_step_handler(msg, choose_author_l3, json.dumps({
        'let': message.text,
        'col': author_collection_name
    }))


def choose_author_l3(message, data):
    db = connect(db_url, db_collection)
    data = json.loads(data)

    if message.text == 'Назад':
        message.text = "по алфавиту"
        choose_author_l1(message)
        return

    new_menu = ['Все дни', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    new_msg = 'Выберите пожалуйста день'

    markup = create_menu(new_menu, back=True)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)
    bot.register_next_step_handler(msg, choose_author_final, json.dumps({
        'name': message.text,
        'let': data['let'],
        'col': data['col']
    }))


@bot.message_handler(content_type=['text'])
def choose_author_final(message, data):
    db = connect(db_url, db_collection)
    data = json.loads(data)

    if message.text == 'Назад':
        message.text = data['let']
        choose_author_l2(message)
        return

    author = db[data['col']].find({'name': data['name']})[0]

    if message.text == 'Все дни':

        schedule = ''
        for day in ['Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
            if day in author:
                schedule_day = author[day]
                if (schedule_day != '') and (schedule_day is not None):
                    schedule = schedule + '\n\n' + day + '\n' + schedule_day
        if schedule != '':
            bot.send_message(message.from_user.id, schedule)
        else:
            bot.send_message(message.from_user.id, 'Ничего нет!')
        bot.register_next_step_handler(message, choose_author_final, json.dumps({
            'name': data['name'],
            'col': data['col'],
            'let': data['let']
        }))

    else:
        if message.text in author:
            if author[message.text] != '':
                bot.send_message(message.from_user.id, author[message.text])
            else:
                bot.send_message(message.from_user.id, 'В этот день ничего нет!')
        else:
            bot.send_message(message.from_user.id, 'В этот день ничего нет!')

        bot.register_next_step_handler(message, choose_author_final, json.dumps({
            'name': data['name'],
            'col': data['col'],
            'let': data['let']
        }))


def start_grushinka():
    try:
        bot.polling(none_stop=True)
    except BaseException as exception:
        print(exception)
        print('Connection refused')
