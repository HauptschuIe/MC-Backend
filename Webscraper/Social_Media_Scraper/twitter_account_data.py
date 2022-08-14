import tweepy
from datetime import datetime
# import sys
# import os 
# sys.path.append("C:\\Users\\gress\\Documents\\master\\WS21\\Jahresprojekt\\Management-Cockpit")
# sys.path.insert(0, os.getcwd())
from Middleware.create import writeTwitterAccountDataIntoDB

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFwiYAEAAAAAT%2BFBntzhf7B5iHLKjIxRHXK728U%3DwMYKEvffrk7uYzAvvvSGjVshixJXebuPMgj8tMlUlgkA8JCWx3"
CONST_SCRAPER_ID = 10

time = datetime.now()

client = tweepy.Client(BEARER_TOKEN)

competitor_twitter_ids = {
    "1": "3823848513",
    "2": "25998749",
    "3": "1136380200",
    "4": "469169735",
    "5": "253934301",
    "6": "1139513777706192896"
}


def scrape_twitter_account_data():

    for id in competitor_twitter_ids.keys():

        response = client.get_user(id=(competitor_twitter_ids[id]),
                                   user_fields=('public_metrics'))

        response = response.data["public_metrics"]

        data_competitor = []

        data_competitor.insert(0, id)
        data_competitor.insert(1, response['followers_count'])
        data_competitor.insert(2, response['following_count'])
        data_competitor.insert(3, response['tweet_count'])
        data_competitor.insert(4, time)
        print(data_competitor)

        writeTwitterAccountDataIntoDB(data_competitor)