from pymongo import MongoClient
import sys

sys.path.append("..")
mapping = {
    "eq":"EarthQuake"
}

# モンゴのクライアント作成
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('localhost', 27017)

def save2db(csv_filepath,db,collection=None):
    from get_tweet_data_util import csv2json
    import os

    # postデータ作る
    collection,data = csv2json(os.path.abspath(csv_filepath))

    # DB作成
    db = client[f'{db}']
    # コレクション(Table)作成
    collection = db[f'{collection}']



    import datetime

    # post = {"author": "Mike",
    #         "text": "My first blog post!",
    #         "tags": ["mongodb", "python", "pymongo"],
    #         "data_added_at": datetime.datetime.utcnow()}

    try:
        # idは自動で一意に振り分けられる
        for post in data:
            result1 = collection.insert_one(data[post])
    except:
        import traceback

        print(traceback.print_exc)

def json2db(data,db,collection):
    # DB作成
    db = client[f'{db}']
    # コレクション(Table)作成
    collection = db[f'{collection}']
    try:
        # idは自動で一意に振り分けられる
        result1 = collection.insert_one(data)
    except:
        import traceback

        print(traceback.print_exc)