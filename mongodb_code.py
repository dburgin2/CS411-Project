import tweepy
from textblob import TextBlob
import jsonpickle
import pandas as pd
import json

import pymongo
from pymongo import MongoClient

consumer_key = 'kgyq2JDeW8g24iYAwrdJCzcIN'
consumer_secret = 'TnEluKJvqiuwgRI1icyczX422P5f05L8ttLRxampd1ZOOjQfAr'
access_key = '1633087315-h2rQ6SZTiraK2PKbofX4AyjfYDNLM6KpPjlgmmT'
access_secret = '0aK7eOYU6NHKAMBG4tk2PlMJuWZVhcYJkXesmXwWGKfvx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
auth.secure = True
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def add_tweets_to_db(curr_ticker, curr_name, num_tweets):

    searchQuery = '$' + curr_ticker
    retweet_filter = '-filter:retweets'

    q = searchQuery + retweet_filter
    tweetsPerQry = 100
    fname = curr_ticker + 'tweets.txt'
    sinceId = None

    max_id = -1
    maxTweets = num_tweets

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(fname, 'w') as f:
        while tweetCount < maxTweets:
            tweets = []
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=q, lang="en", count=tweetsPerQry,
                                                tweet_mode="extended")
                    else:
                        new_tweets = api.search(q=q, lang="en", count=tweetsPerQry,
                                                since_id=sinceId, tweet_mode="extended")
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=q, lang="en", count=tweetsPerQry,
                                                max_id=str(max_id - 1), tweet_mode="extended")
                    else:
                        new_tweets = api.search(q=q, lang="en", count=tweetsPerQry,
                                                max_id=str(max_id - 1), since_id=sinceId,
                                                tweet_mode="extended")

                if not new_tweets:
                    print("No more tweets found.")
                    break
                for tweet in new_tweets:
                    f.write(str(tweet.full_text.replace('\n', '').encode("utf-8")))
                    f.write(str(tweet.created_at) + "\n")

                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id

            except tweepy.TweepError as e:
                print("Some error" + str(e))
                break

            for i in tweets:
                print(i.created_at)

    print("Downloaded {0} tweets, saved to {1}".format(tweetCount, fname))

    # CHANGE TO CORRECT PATH HERE IF NOT ALREADY CORRECT
    f = open(fname)

    # Split txt file into list containing a tweet in each entry
    tweets_list = f.readlines()

    # Get rid of the b at the beginning of each tweet
    for i in range(0, len(tweets_list)):
        tweets_list[i] = (tweets_list[i])[1:]

    mongo_client = MongoClient()
    # CHANGE NAME OF DATABASE IF NOT CORRECT OR NOT WHAT YOU WANT IT TO BE CALLED
    db = mongo_client.cs411_project_db
    coll = db.cs411_project_coll

    # Assign values for time, date, and tweet, then insert tweets into MongoDB collection
    for tweets in tweets_list:
        time = tweets[-9:-1]
        date = tweets[-20:-10]
        tweet = tweets[:-21]

        dict = {
            "company_name": curr_name,
            "ticker": curr_ticker,
            "tweet": tweet,
            "date": date,
            "time": time
        }

        result_object = coll.insert_one(dict).inserted_id

    for doc in coll.find():
        print(doc)

add_tweets_to_db('AMD', 'AMD', 100)
add_tweets_to_db('JMIA', 'JMIA', 100)
add_tweets_to_db('PLUG', 'PLUG', 100)
add_tweets_to_db('M', 'M', 100)
add_tweets_to_db('PFE', 'PFE', 100)
add_tweets_to_db('BAC', 'BAC', 100)
add_tweets_to_db('LI', 'LI', 100)
add_tweets_to_db('XPEV', 'XPEV', 100)
add_tweets_to_db('F', 'F', 100)
add_tweets_to_db('FSR', 'FSR', 100)
add_tweets_to_db('VALE', 'VALE', 100)
add_tweets_to_db('ITUB', 'ITUB', 100)
x = "TSLA"
add_tweets_to_db(x, x, 100)
x = "MRNA"
add_tweets_to_db(x, x, 100)
x = "AAPL"
add_tweets_to_db(x, x, 100)
x = "SRNE"
add_tweets_to_db(x, x, 100)
x = "CCL"
add_tweets_to_db(x, x, 100)
x = "WORK"
add_tweets_to_db(x, x, 100)
x = "GE"
add_tweets_to_db(x, x, 100)
x = "AAL"
add_tweets_to_db(x, x, 100)
x = "FCEL"
add_tweets_to_db(x, x, 100)
x = "NIO"
add_tweets_to_db(x, x, 100)
x = "PLTR"
add_tweets_to_db(x, x, 100)
x = "SPCE"
add_tweets_to_db(x, x, 100)
x = "CSCO"
add_tweets_to_db(x, x, 100)
x = "ET"
add_tweets_to_db(x, x, 100)
x = "MSFT"
add_tweets_to_db(x, x, 100)
x = "OXY"
add_tweets_to_db(x, x, 100)
x = "UAL"
add_tweets_to_db(x, x, 100)
x = "C"
add_tweets_to_db(x, x, 100)
x = "MRO"
add_tweets_to_db(x, x, 100)
x = "AZN"
add_tweets_to_db(x, x, 100)
x = "XOM"
add_tweets_to_db(x, x, 100)
x = "INTC"
add_tweets_to_db(x, x, 100)
x = "T"
add_tweets_to_db(x, x, 100)
x = "DKNG"
add_tweets_to_db(x, x, 100)
x = "PBR"
add_tweets_to_db(x, x, 100)
x = "GOLD"
add_tweets_to_db(x, x, 100)
x = "NCLH"
add_tweets_to_db(x, x, 100)
x = "BBD"
add_tweets_to_db(x, x, 100)
x = "INO"
add_tweets_to_db(x, x, 100)
x = "COTY"
add_tweets_to_db(x, x, 100)

