# -*- coding: utf-8 -*-

import urllib.request as ulib

from bs4 import BeautifulSoup


def get_author_schedule_by_day(url, day):
    request = ulib.Request(url)
    request.add_header('Accept-Encoding', 'utf-8')
    response = ulib.urlopen(request)
    soup = BeautifulSoup(response, 'lxml')

    raw_data = soup.find_all('div', attrs={'class': 'view-content'})

    if not raw_data:
        return
    else:
        raw_data = raw_data[0].text

    get_element = False
    first_item = True
    schedule = ''
    new_event = 0

    wrong_days = ['Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    wrong_days.remove(day)

    for item in raw_data.split():
        if item == day:
            get_element = True
            continue
        elif item in wrong_days:
            get_element = False
        elif get_element:
            if (item[0] in ['0', '1', '2']) and (':' in item):
                new_event += 1
            if new_event % 3 == 0:
                schedule = schedule + '\n' + item
                new_event = 1
            else:
                if not first_item:
                    schedule = schedule + ' ' + item
                else:
                    schedule = item
                    first_item = False

    return schedule


def get_scene_schedule(url):
    pass

# string = get_author_schedule_by_day("https://scn.grushinka.ru/guest/gorodnickiy-aleksandr", 'Пятница')
# print(string)
# print(string.split())

# 3 -
