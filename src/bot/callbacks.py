from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


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
