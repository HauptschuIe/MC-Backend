from HelperClasses.fact_SimilarWeb_Zielgruppendemografie import Fact_SimilarWeb_Zielgruppendemografie
from HelperClasses.fact_SimilarWeb_Visitor import Fact_SimilarWeb_Visitor
from HelperClasses.scraper import Scraper
from Middleware.read import url_rueckgabe
from Middleware.create import writeResultsIntoDB
from DataTransformation.transformation import *
from Middleware.dbOperations_Read import *
from Middleware.dbOperations_Insert import *
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import seleniumwire.undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
import time
import datetime
import requests
import logging
import traceback
"""
SCRAPER SETTINGS
You need to define the following values below:
- API_KEY --> Find this on your dashboard, or signup here to create a 
                free account here https://dashboard.scraperapi.com/signup
- RETRY_TIMES  --> We recommend setting this to 2-3 retries, in case a request fails. 
                For most sites 95% of your requests will be successful on the first try,
                and 99% after 3 retries. 
"""
API_KEY = '6436f8c4d2f01d70287dec5bb00fd09c'
# API_KEY = '4fe002d2db16c9395b27c3fb9d195b6b'
NUM_RETRIES = 4

proxy_options = {
    'proxy': {
        'http':
        f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'https':
        f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'no_proxy': 'localhost,127.0.0.1'
    }
}


def status_code_first_request(performance_log):
    """
        Selenium makes it hard to get the status code of each request,
        so this function takes the Selenium performance logs as an input
        and returns the status code of the first response.
    """
    for line in performance_log:
        try:
            json_log = json.loads(line['message'])
            if json_log['message']['method'] == 'Network.responseReceived':
                return json_log['message']['params']['response']['status']
        except:
            pass
    return json.loads(response_recieved[0]['message'])['message']['params']['response']['status']


class Scraper_SimilarWeb(Scraper):

    def scrape(self):
        ## optional --> define Selenium options
        options = webdriver.ChromeOptions()
        #options.add_argument("start-maximized")
        #options.add_argument("enable-automation")
        #options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        #options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        #options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-sh-usage')
        options.page_load_strategy = 'normal'

        ## enable Selenium logging
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        ## set up Selenium Chrome driver
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                                options=options,
                                desired_capabilities=caps,
                                seleniumwire_options=proxy_options)

        visitor_facts = []
        marketing_channels_facts = []
        keywords_facts = []
        zielgruppendemografie_facts = []


        for dataSource in self.dataSources:
            try:
                for _ in range(NUM_RETRIES):
                    try:
                        driver.get(dataSource.url)
                        performance_log = driver.get_log('performance')
                        status_code = status_code_first_request(performance_log)
                        time.sleep(20)
                        if status_code in [200, 404]:
                            # escape for loop if the API returns a successful response
                            break
                    except requests.exceptions.ConnectionError:
                        driver.close()

                if status_code == 200:
                    # feed HTML response into BeautifulSoup
                    html_source = driver.page_source
                    soup = BeautifulSoup(html_source, "html.parser")
                    with open(f"./Webscraper/Similarweb/scraped_1.txt", "w", encoding="utf-8") as file:
                        file.write(str(soup))
                    # Scrape visitor_facts
                    try:
                        visitor_facts += self.scrape_visitors(soup, dataSource.competitorId)
                    except Exception as scrape_visitors_error:
                        print("Exception in scrape_visitors Scraper")
                        logging.error(traceback.format_exc())
                    # Scrape marketing_channels_facts
                    try:
                        marketing_channels_facts += self.scrape_marketing_channels(soup, dataSource.competitorId)
                    except Exception as scrape_marketing_channels_error:
                        print("Exception in scrape_marketing_channels Scraper")
                        logging.error(traceback.format_exc())
                    # Scrape keywords_facts
                    try:
                        keywords_facts += self.scrape_keywords(soup, dataSource.competitorId)
                    except Exception as scrape_keywords_error:
                        print("Exception in scrape_keywords Scraper")
                        logging.error(traceback.format_exc())
                    # Scrape Zielgruppendemografie
                    #try:
                    #    zielgruppendemografie_facts += self.scrape_zielgruppendemografie(soup, dataSource.competitorId)
                    #except Exception as scrape_zielgruppendemografie_error:
                    #    print("Exception in scrape_zielgruppendemografie Scraper")
                    #    logging.error(traceback.format_exc())

                    print("successfully scraped data from ", dataSource.url)
                    time.sleep(20)
                else:
                    raise ConnectionError(
                        "Not able to successfully connect to SimilarWeb for " + dataSource.url)

            except ConnectionError:
                logging.error(traceback.format_exc())
            finally:
                time.sleep(20)

        return visitor_facts, marketing_channels_facts, keywords_facts, zielgruppendemografie_facts

    def scrape_visitors(self, soup, competitorId):
        facts = []

        fact_SimilarWeb_Visitor = Fact_SimilarWeb_Visitor()
        fact_SimilarWeb_Visitor.competitorId = competitorId
        fact_SimilarWeb_Visitor.timestamp = datetime.datetime.now()
        fact_SimilarWeb_Visitor.fact_timestamp = transformMonthYearToTimestamp(soup.select("p.data-header__date")[0].text)

        #Scrape totalVisitors, avgVisitDuration, pagesPerVisit, jumpOffRate
        fact_SimilarWeb_Visitor.totalVisitors = transformTotalVisitorsToInt(soup.select(
                "div.wa-traffic__engagement > div:nth-child(1) > span.wa-traffic__engagement-item-value"
            )[0].text)
        fact_SimilarWeb_Visitor.avgVisitDuration = transformAvgVisitDurationToSeconds(soup.select(
                "div.wa-traffic__engagement > div:nth-child(3) > span.wa-traffic__engagement-item-value"
            )[0].text)
        fact_SimilarWeb_Visitor.pagesPerVisit = soup.select(
            "div.wa-traffic__engagement > div:nth-child(5) > span.wa-traffic__engagement-item-value"
        )[0].text
        fact_SimilarWeb_Visitor.jumpOffRate = transformJumpOffRateToFloat(soup.select(
                "div.wa-traffic__engagement > div:nth-child(4) > span.wa-traffic__engagement-item-value"
            )[0].text)
        facts.append(fact_SimilarWeb_Visitor)

        return facts

    def scrape_marketing_channels(self, soup, competitorId):
        facts = []

        #Key = Channel, Value = Index of occurence in HTML
        tagDict = {
            "Direct": 0,
            "Referral": 1,
            "Search": 2,
            "Social": 3,
            "Mail": 4,
            "Ads": 5
        }

        for key in tagDict:
            fact_SimilarWeb_Marketing_Channels = Fact_SimilarWeb_Marketing_Channels()
            fact_SimilarWeb_Marketing_Channels.competitorId = competitorId
            fact_SimilarWeb_Marketing_Channels.timestamp = datetime.datetime.now()

            fact_SimilarWeb_Marketing_Channels.marketing_channel = key
            fact_SimilarWeb_Marketing_Channels.share = transformShareToFloat(soup.select("tspan.wa-traffic-sources__channels-data-label")[tagDict[key]].text)
            fact_SimilarWeb_Marketing_Channels.fact_timestamp = transformMonthYearToTimestamp(soup.select("p.data-header__date")[0].text)
            facts.append(fact_SimilarWeb_Marketing_Channels)

        return facts

    def scrape_keywords(self, soup, competitorId):
        facts = []

        keyword_rows = soup.select(
            "div.wa-keywords__vectors-list > div.wa-vectors-list > div.wa-vectors-list__items > span.wa-vectors-list__item > span.wa-vectors-list__item-row"
        )

        for keyword_row in keyword_rows:
            fact_SimilarWeb_Keywords = Fact_SimilarWeb_Keywords()
            fact_SimilarWeb_Keywords.competitorId = competitorId
            fact_SimilarWeb_Keywords.timestamp = datetime.datetime.now()

            fact_SimilarWeb_Keywords.keyword = keyword_row.select("span.wa-vectors-list__item-title")[0].text
            fact_SimilarWeb_Keywords.share = transformShareToFloat(keyword_row.select("span.wa-vectors-list__item-value")[0].text)
            fact_SimilarWeb_Keywords.fact_timestamp = transformMonthYearToTimestamp(soup.select("p.data-header__date")[0].text)
            facts.append(fact_SimilarWeb_Keywords)

        return facts

    def scrape_zielgruppendemografie(self, soup, competitorId):
        facts = []

        fact_SimilarWeb_Zielgruppendemografie = Fact_SimilarWeb_Zielgruppendemografie()
        fact_SimilarWeb_Zielgruppendemografie.competitorId = competitorId
        fact_SimilarWeb_Zielgruppendemografie.timestamp = datetime.datetime.now()
        fact_SimilarWeb_Zielgruppendemografie.fact_timestamp = transformMonthYearToTimestamp(soup.select("p.data-header__date")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.female = transformShareToFloat(soup.select("#demographics > div > div > div.wa-demographics__main-content > div.wa-demographics__gender > ul > li.wa-demographics__gender-legend-item.wa-demographics__gender-legend-item--female > span.wa-demographics__gender-legend-item-value")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.male = transformShareToFloat(soup.select("#demographics > div > div > div.wa-demographics__main-content > div.wa-demographics__gender > ul > li.wa-demographics__gender-legend-item.wa-demographics__gender-legend-item--male > span.wa-demographics__gender-legend-item-value")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.firstAge = transformShareToFloat(soup.select("g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-tracker > g.highcharts-label.highcharts-data-label.highcharts-data-label-color-0 > text > tspan")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.secondAge = transformShareToFloat(soup.select("g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-tracker > g.highcharts-label.highcharts-data-label.highcharts-data-label-color-1 > text > tspan")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.thirdAge = transformShareToFloat(soup.select("g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-tracker > g.highcharts-label.highcharts-data-label.highcharts-data-label-color-2 > text > tspan")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.fourthAge = transformShareToFloat(soup.select("g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-tracker > g.highcharts-label.highcharts-data-label.highcharts-data-label-color-3 > text > tspan")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.fifthAge = transformShareToFloat(soup.select("g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-tracker > g.highcharts-label.highcharts-data-label.highcharts-data-label-color-4 > text > tspan")[0].text)
        fact_SimilarWeb_Zielgruppendemografie.sixthAge = transformShareToFloat(soup.select("g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-tracker > g.highcharts-label.highcharts-data-label.highcharts-data-label-color-5 > text > tspan")[0].text)

        facts.append(fact_SimilarWeb_Zielgruppendemografie)

        return facts

