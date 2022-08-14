from datetime import datetime
from Middleware.create import writeYoutubeChannelDataIntoDB
import googleapiclient.discovery
# import sys
# import os
# sys.path.append("C:\\Users\\gress\\Documents\\master\\WS21\\Jahresprojekt\\Management-Cockpit")
# sys.path.insert(0, os.getcwd())


API_KEY = "AIzaSyAAX1u1cMTMRqWBcCgb889vEgF-XofHvCw"
CONST_SCRAPER_ID = 9
time = datetime.now()

competitor_youtube_ids = {
    "1": 'UCkLXELm63_pH7L-r-548kig',
    "2": 'UClqYgJyT51vGS2JavNoQaRQ',
    "3": 'UCB5InFXkLo7xvnr6FN8pwuQ',
    "4": 'UCIgrnoQbqeIosRTAlFLKa8g',
    "5": 'UC-OOL0hJdwjXH5nDTwcxeLQ',
    "6": 'UCAFoyaEsLHFxTO96BGWvs9g'
}


def scrape_youtube_channel_data():
    
    api_service_name = 'youtube'
    api_version = 'v3'

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    for id in competitor_youtube_ids.keys():

        value = competitor_youtube_ids[id]
        request = youtube.channels().list(
            part="statistics",
            id=value
        )
        response = request.execute()
        response = response["items"][0]["statistics"]

        data_competitor = []

        data_competitor.insert(0, id)
        data_competitor.insert(1, response['viewCount'])
        data_competitor.insert(2, response['subscriberCount'])
        data_competitor.insert(3, response['videoCount'])
        data_competitor.insert(4, time)
        print(data_competitor)

        writeYoutubeChannelDataIntoDB(data_competitor)