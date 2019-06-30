# -*- coding: utf-8 -*-

# from data.static import scenes
from db.mongo import connect
from config import db_url, db_collection
from utils.parser import get_author_schedule_by_day, get_scene_schedule_by_day


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
