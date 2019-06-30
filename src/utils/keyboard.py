# -*- coding: utf-8 -*-

from telebot import types


def create_menu(array, back=True):
    """
    This function allows to creat menu of buttons.
    array - the list of string
    back - back button, if true, add a button back. Default back=True
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if len(array) == 1:
        markup.row(array[0])
    else:
        while len(array) > 0:
            try:
                cut = array[:2]
                markup.row(cut[0], cut[1])
                del array[:2]

                if len(array) == 1:
                    markup.row(array[0])
                    break
            except:
                print('WTF')

    if back:
        markup.row('Назад')

    return markup
