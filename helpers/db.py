import os

import pymongo
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DB")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def load_database():
    mongo = pymongo.MongoClient(DB, username=DB_USER, password=DB_PASS)
    return mongo.rcdb.webscraper
