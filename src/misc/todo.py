# @bot.message_handler(commands=['сейчас'])
# @bot.message_handler(commands=['сегодня'])
# @bot.message_handler(commands=['завтра'])

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def text(message):
#    bot.send_message(message.chat.id, 'Lean session is not started yet')

@bot.message_handler(commands=['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Наш сайт', url='https://habrahabr.ru')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)

@bot.message_handler(commands=['расписание'])
def schedule(message):
    author = extract_arg(message.text)[0] + ' ' + extract_arg(message.text)[1]
    print(author)

    print(authors_list)

    # bot.send_message(message.chat.id, authors_list)

#@bot.message_handler(commands=['буква'])
#def authors(message):
#    letter = extract_arg(message.text)[0]
    # bot.send_message(message.chat.id, prepare_msg([*get_authors_by_letter(letter)]))

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#    bot.reply_to(message, "Howdy, how are you doing?")


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'add':
        bot.answer_callback_query(callback_query_id=call.id, text='Hello world')


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message the developer', url='telegram.me/artiomtb'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) To receive a list of available currencies press /exchange.\n',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['сцены'])
def scenes(message):
    bot.send_message(message.chat.id, prepare_list_msg(scenes_list))


@bot.message_handler(commands=['авторы'])
def authors(message):
    bot.send_message(message.chat.id, prepare_list_msg(authors_list))


### авторы
#authors_list = get_authors_list()
#scenes_list = get_scenes_list()
