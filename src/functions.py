# -*- coding: utf-8 -*-

import json

#from data.static import authors, scenes, dates
#from utils.parser import generate_author_schedule

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_author_code(author):
    return get_authors_map()[author]


def get_authors_map_by_letter(letter):
    return authors[letter]


def callback_author_time_2(bot, query, author_url):
    message = query.message
    bot.edit_message_text(
        'generate_author_schedule(author_url)',
        message.chat.id,
        message.message_id,
        parse_mode='HTML'
    )


def callback_author_time(bot, query, author):
    bot.answer_callback_query(query.id)

    message = query.message

    keyboard = InlineKeyboardMarkup()

    row = []
    for date in dates:
        row.append(InlineKeyboardButton(date, callback_data=json.dumps({
            'author_data': 'todo'
        })))

    keyboard.row(*row)

    bot.edit_message_text(
        'todo',
        message.chat.id,
        message.message_id,

        reply_markup=keyboard,
        parse_mode='HTML'
    )


def callback_authors_by_letter(bot, query, letter):
    bot.answer_callback_query(query.id)

    message = query.message

    keyboard = InlineKeyboardMarkup()

    row = []
    for author in get_authors_list_by_letter(letter):
        row.append(InlineKeyboardButton(author, callback_data=json.dumps({
            'author': get_author_code(author)
        })))

    keyboard.row(*row)

    bot.edit_message_text(
        'todo',
        message.chat.id,
        message.message_id,
        reply_markup=keyboard,
        parse_mode='HTML'
    )


def get_authors_list_by_letter(letter):
    return [*get_authors_map_by_letter(letter)]


def get_authors_map():
    authors_map = {}
    for letter in authors:
        authors_map = {**authors_map, **(get_authors_map_by_letter(letter))}
    return authors_map


def get_authors_list():
    return [*get_authors_map()]


def get_scenes_list():
    return [*scenes]


def extract_arg(arg):
    return arg.split()[1:]


def prepare_list_msg(obj):
    msg = ""
    for item in obj:
        msg += '\n' + str(item)
    return msg


def get_letters():
    return [*authors]
