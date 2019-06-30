# -*- coding: utf-8 -*-


from threading import Thread

from utils.updater import update_scenes_daemon, update_authors_daemon
from bot.bot import start_grushinka

if __name__ == '__main__':
    update_authors_proccess = Thread(target=update_scenes_daemon, args=())
    update_authors_proccess.start()

    update_authors_proccess = Thread(target=update_authors_daemon, args=())
    update_authors_proccess.start()

    telegram_bot_proccess = Thread(target=start_grushinka, args=())
    telegram_bot_proccess.start()
