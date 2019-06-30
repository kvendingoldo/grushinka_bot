# -*- coding: utf-8 -*-

import json

#from data.static import authors, scenes, dates
#from utils.parser import generate_author_schedule


def get_author_code(author):
    return get_authors_map()[author]


def get_authors_map_by_letter(letter):
    return authors[letter]





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
