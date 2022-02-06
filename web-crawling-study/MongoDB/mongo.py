from pymongo import MongoClient
import json
import logging

with open("./sojoong.json", 'rt', encoding='UTF8') as news_json:
    data = json.load(news_json)

# print(data)
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.newsDB.sojoong


db.insert_many(data)
print(f'inserted {len(data)} articles')


    