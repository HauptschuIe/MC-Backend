import datetime as dt
from datetime import date
from datetime import datetime
import tweepy as tw
from transformers import pipeline
import re
# USE FOR LOCAL TEST
import sys
import os
sys.path.append("C:\\Users\\gress\\Documents\\master\\WS21\\Jahresprojekt\\Management-Cockpit")
sys.path.insert(0, os.getcwd())
import Middleware.create

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFwiYAEAAAAAT%2BFBntzhf7B5iHLKjIxRHXK728U%3DwMYKEvffrk7uYzAvvvSGjVshixJXebuPMgj8tMlUlgkA8JCWx3"
CONST_SCRAPER_ID = 11

competitor_twitter_ids = {
    "1": "3823848513",
    "2": "25998749",
    "3": "1136380200",
    "4": "469169735",
    "5": "253934301",
    "6": "1139513777706192896"
}

client = tw.Client(BEARER_TOKEN)

today = date.today()
yesterday = today - dt.timedelta(days=1)

min_time = datetime.min.time()
max_time = datetime.max.time()

# Use this once for all tweets from 01.10.2021
# tweets_min_date = dt.datetime(2021, 10, 1, 0, 0, 0)
tweets_min_date = datetime.combine(yesterday, min_time)
tweets_max_date = datetime.combine(yesterday, max_time)

# Model for sentiment analysis
model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis",
                          model=model_path,
                          tokenizer=model_path)


def clean_text(tweet):
    tweet = tweet.replace("\n", " ")
    tweet = re.sub(r'http\S+', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'@\\S+', '', tweet, flags=re.MULTILINE)
    tweet = tweet.replace("0", " null").replace("1", " eins").replace(
        "2", " zwei").replace("3", " drei").replace("4", " vier").replace(
            "5", " fünf").replace("6",
                                  " sechs").replace("7", " sieben").replace(
                                      "8", " acht").replace("9", " neun")
    tweet = re.sub(r'[^A-Za-züöäÖÜÄß ]', '', tweet)
    tweet = ' '.join(
        tweet.split())  #substitute multiple whitespace with single whitespace
    tweet = tweet.strip().lower()
    return tweet

def scrape_twitter_mentions_data():
    
    for id in competitor_twitter_ids.keys():

        tweets = tw.Paginator(client.get_users_mentions,
                              id=competitor_twitter_ids[id],
                              start_time=tweets_min_date,
                              end_time=tweets_max_date,
                              tweet_fields=['created_at'],
                              max_results=100).flatten(limit=10000)

        for tweet in tweets:
            
            # 0 = competitor id, 1 = creation id, 2 = tweet text
            data = []
            data.insert(0, id)
            data.insert(1, tweet.created_at)
            data.insert(2, tweet.text)
            sentiment_object = sentiment_task(clean_text(tweet.text))
            sentiment = sentiment_object[0]["label"]
            confidence = sentiment_object[0]["score"]
            data.insert(3, sentiment)
            data.insert(4, confidence)
            Middleware.create.writeTwitterCommentsDataIntoDB(data)

scrape_twitter_mentions_data()