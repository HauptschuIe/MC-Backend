from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import transformMonth
from selenium import webdriver as wd
from HelperClasses.scraper import Scraper
from HelperClasses.fact_customer_review_new import Fact_CustomerReviewNew
import json
import requests
import time

# Initialize Header Information
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.132 Safari/537.36'
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
accept_en = "gzip, deflate, br"
accept_lan = "en-US,en;q=0.9"
cache_con = "max-age=0"
cokies = ""
down_link = "0.35"
headers = {'accept': accept,
           'accept-encoding': accept_en,
           'accept-language': accept_lan,
           'cache-control': cache_con,
           'cache': cokies,
           'user-agent': user_agent, }



class TrustpilotScraperPerSource(Scraper):
    def scrape_customer_review_source(self):
        facts = []
        for locationSource in self.dataSources:

            # Http Request
            content = requests.get(locationSource.url, headers=headers)
            soup = BeautifulSoup(content.text, "html.parser")

            data = json.loads(soup.find('script', id='__NEXT_DATA__').string)

            quellen = ["automatic","manual","organic","redirected","all"]
            bewertung = ["one", "two", "three", "four", "five"]
            for child in quellen:

                dataO = data['props']['pageProps']['reviewStatistics']['monthlyDistribution'][child]['one']
                dataT = data['props']['pageProps']['reviewStatistics']['monthlyDistribution'][child]['two']
                dataTh = data['props']['pageProps']['reviewStatistics']['monthlyDistribution'][child]['three']
                dataF = data['props']['pageProps']['reviewStatistics']['monthlyDistribution'][child]['four']
                dataFi = data['props']['pageProps']['reviewStatistics']['monthlyDistribution'][child]['five']

                for (key,value),(key2,value2),(key3,value3),(key4,value4),(key5,value5) in zip(dataO.items(), dataT.items(), dataTh.items(), dataF.items(), dataFi.items()):
                    fact_customer_review = Fact_CustomerReviewNew()
                    fact_customer_review.competitor_id = locationSource.competitorId
                    fact_customer_review.timestamp = datetime.now()
                    date = key.split("-")
                    fact_customer_review.year = date[0]
                    fact_customer_review.month = transformMonth(date[1])
                    if(child =="all"):
                        fact_customer_review.sources_of_evaluations_id = 1
                    elif(child =="organic"):
                        fact_customer_review.sources_of_evaluations_id = 2
                    elif (child == "automatic"):
                        fact_customer_review.sources_of_evaluations_id = 3
                    elif (child == "manual"):
                        fact_customer_review.sources_of_evaluations_id = 4
                    elif (child == "redirected"):
                        fact_customer_review.sources_of_evaluations_id = 5

                    fact_customer_review.excellent = value5
                    fact_customer_review.good = value4
                    fact_customer_review.acceptable = value3
                    fact_customer_review.deficient = value2
                    fact_customer_review.insufficient = value

                    facts.append(fact_customer_review)

        return facts

