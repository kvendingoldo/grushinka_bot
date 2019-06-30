# -*- coding: utf-8 -*-

import sys
import json

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from db.mongo import connect

sys.path.append('../resources/')
from config import db_url, db_collection


def callback_author_l3(bot, query, letter_collection, author_id, day):
    message = query.message

    # db[letter_collection].find({'_id': author_id})[day]

    bot.edit_message_text(
        'generate_author_schedule(author_url)',
        message.chat.id,
        message.message_id,
        parse_mode='HTML'
    )


def callback_author_l2(bot, query, letter_collection, author_id):
    db = connect(db_url, db_collection)

    bot.answer_callback_query(query.id)

    message = query.message

    keyboard = InlineKeyboardMarkup()

    row = []
    for day in db['days'].find():
        row.append(InlineKeyboardButton(day, callback_data=json.dumps({
            'cat': 'aut_l3',
            'col': letter_collection,
            'aut_id': author_id,
            'day': day
        })))

    keyboard.row(*row)

    bot.edit_message_text(
        'todo',
        message.chat.id,
        message.message_id,

        reply_markup=keyboard,
        parse_mode='HTML'
    )




