from numpy import rot90
import tweepy as tw
import datetime as dt
from datetime import date
from datetime import datetime
#USE FOR LOCAL DEBUG
# import sys
# import os
# sys.path.append("C:\\Users\\gress\\Documents\\master\\WS21\\Jahresprojekt\\Management-Cockpit")
# sys.path.insert(0, os.getcwd())
from Middleware.create import writeTwitterTweetsDataIntoDB

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFwiYAEAAAAAT%2BFBntzhf7B5iHLKjIxRHXK728U%3DwMYKEvffrk7uYzAvvvSGjVshixJXebuPMgj8tMlUlgkA8JCWx3"

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

# Use this in production for tweets from yesterday
tweets_min_date = datetime.combine(yesterday, min_time)
tweets_max_date = datetime.combine(yesterday, max_time)



def scrape_twitter_tweet_data():

    for id in competitor_twitter_ids.keys():

        tweets = tw.Paginator(
            client.get_users_tweets,
            id=competitor_twitter_ids[id],
            exclude='retweets',
            start_time=tweets_min_date,
            end_time=tweets_max_date,
            tweet_fields=[
                'created_at',
                'lang',
                'public_metrics',
            ],
            max_results=100
        ).flatten(limit=100000)

        for tweet in tweets:
            data = []
            data.insert(0, id)
            data.insert(1, tweet.text)
            data.insert(2, tweet.created_at)
            data.insert(3, tweet.public_metrics['retweet_count'])
            data.insert(4, tweet.public_metrics['reply_count'])
            data.insert(5, tweet.public_metrics['like_count'])
            data.insert(6, tweet.public_metrics['quote_count'])
            writeTwitterTweetsDataIntoDB(data)

# scrape_twitter_tweet_data()