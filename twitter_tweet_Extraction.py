from data_pre_processing import data_preprocessing
import tweepy
import datetime
import csv
import os
import pandas as pd
import shutil
import re
####input your credentials here
#Rakesh Access Keys
consumer_key = 'P3bEE8Y32TPgxJi9WmBDdunBq'
consumer_secret = 'nUpIaP4COuOjVEva97zVhTcZaRgyb5HuRf6IESIOmLmCMcEoMU'
access_token = '1504203727196114955-i9rffWfgWHORCuVkYBKwKXOVIoEWgr'
access_token_secret = 'OY7xarccu69Bhxvao7ZfgTXudKadJDuMGrfM3JHA7B87X'

# consumer_key = 'mGEigvVaEmKb2hvHRLRDZIAO7'
# consumer_secret = 'Ggfu91IRh4Vd5Ljc4i7gOtUzMbT6o7nGZLNOZCDYWLLN2nd8Ki'
# access_token = '1505247723351592963-ikEDAJpJLmUgqeeASwFtF7J8VbnlNh'
# access_token_secret = 'HLGDd2QakieiUtiFonY3CNTO275Mokjfjft2bUImQIqav'


def getTweets(stock):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    # shutil.rmtree( "./output", ignore_errors=False, onerror=None)
    # os.mkdir("./output")

    
    output = []
    for tweet in tweepy.Cursor(api.search_tweets,q=("#" + stock),lang="en",count=100).items():
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            tweet.text = re.sub(r'[^\x00-\x7F]+',' ', tweet.text)
            text = tweet.text
            favourite_count = tweet.favorite_count
            retweet_count = tweet.retweet_count
            created_at = tweet.created_at
            line = {'text' : text, 'favourite_count' : favourite_count, 'retweet_count' : retweet_count, 'created_at' : created_at}
            output.append(line)
    df = pd.DataFrame(output)
    df.to_csv("./output/" + stock + ".csv")
    data = pd.read_csv(r"./output/" + stock + ".csv" , encoding = 'utf8')
    return data