# -*- coding: utf-8 -*-

import sys
import time

from db.mongo import connect
from utils.parser import get_author_schedule_by_day, get_scene_schedule_by_day

sys.path.append('../resources/')
from config import db_url, db_collection


def update_scenes_daemon(sleep_time_second=3600):
    while True:
        update_scenes()
        time.sleep(sleep_time_second)


def update_scenes():
    db = connect(db_url, db_collection)

    for scene in db['scenes'].find():
        for day in db['days'].find():
            schedule = get_scene_schedule_by_day(scene['url'], day['name'])
            if schedule is not None:
                db['scenes'].update_one(
                    scene,
                    {"$set":
                        {
                            day['name']: schedule
                        }
                    },
                    upsert=False
                )


def update_authors_daemon(sleep_time_second=3600):
    while True:
        update_authors()
        time.sleep(sleep_time_second)


def update_authors():
    db = connect(db_url, db_collection)

    for letter in db['letters'].find():

        author_collection = db[letter['collection']]
        for author in author_collection.find():
            for day in db['days'].find():
                schedule = get_author_schedule_by_day(author['url'], day['name'])

                if schedule is not None:
                    author_collection.update_one(
                        author,
                        {"$set":
                            {
                                day['name']: schedule
                            }
                        },
                        upsert=False
                    )
