import pymongo
from pymongo import MongoClient
import pandas as pd
file = pd.read_csv("TweetsWithSentiment.csv", engine = "python", header = None)
file.rename(columns = {0 : '_id', 1 : 'company_name', 2 : 'ticker', 3 : 'tweet', 4 : 'date',
                       5 : 'time', 6 : 'sentiment'}, inplace = True)
mongo_client = MongoClient()
db = mongo_client.sentiment_tweets_db
coll = db.sentiment_tweets_coll
insert_data = file.to_dict(orient = "records")
coll.insert_many(insert_data)