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
def callback_author_l0(message):



    db = connect(db_url, db_collection)
    keyboard = types.InlineKeyboardMarkup()

    row = []
    for letter in db['letters'].find():
        row.append(types.InlineKeyboardButton(
            text=letter['name'],
            # todo
            callback_data=json.dumps({
                #    'cat': 'aut_l1',
            })
        ))

    keyboard.row(*row)

    msg = bot.send_message(message.chat.id, 'Выберите букву:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, callback_author_l1)




def callback_author_l1(message):
    print('HERE')
    db = connect(db_url, db_collection)

    # print(query)
    # print(query.text)

    # bot.answer_callback_query(query.id)

    # message = query.message

    keyboard = InlineKeyboardMarkup()

    row = []

    for author in db['l21'].find():
        row.append(InlineKeyboardButton(
            text=author['name'],
            callback_data=json.dumps({
                #    'cat': 'aut_l2',
                #    'col': letter_collection,
                #    'aut_id': str(author['_id'])
            })
        ))

    keyboard.row(*row)

    bot.edit_message_text(
        'todo',
        message.chat.id,
        message.message_id,
        reply_markup=keyboard,
        parse_mode='HTML'
    )


# @bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_CHOOSE_GOOD)
# def intermediate_choise(message):
#    user_id = message.from_user.id

# if message.text == "Назад":
#   db_users.set_state(user_id, config.S_GET_CAT)
#  get_categories(message)
