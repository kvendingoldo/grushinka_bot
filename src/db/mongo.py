# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


def connect(url, db_name):
    db = None

    try:
        client = MongoClient(url, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        db = client[db_name]
    except ServerSelectionTimeoutError:
        print("server is down.")

    return db
