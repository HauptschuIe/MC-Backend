import requests
from bs4 import BeautifulSoup
from geopy import geocoders
from geopy.geocoders import Nominatim
import urllib3
from datetime import datetime
from selenium import webdriver as wd
from webdriver_manager.chrome import ChromeDriverManager
import time
from HelperClasses.scraper import Scraper
from HelperClasses.fact_location_informations import Fact_LocationInformations

urllib3.disable_warnings()

# Initialize Header Information
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.132 Safari/537.36'
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8," \
         "application/signed-exchange;v=b3;q=0.9 "
accept_en = "gzip, deflate, br"
accept_lan = "en-US,en;q=0.9"
cache_con = "max-age=0"
cokies = ""
down_link = "0.35"
headers = {'accept': accept,
           'accept-language': accept_lan,
           'cache-control': cache_con,
           'cache': cokies,
           'user-agent': user_agent, }


class EuronicsLocationsScraper(Scraper):

    def scrape_location_details(self):
        facts = []
        for locationSource in self.dataSources:

            chrome_options = wd.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('log-level=3')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = wd.Chrome(ChromeDriverManager().install(),options=chrome_options)

            driver.get(locationSource.url)
            time.sleep(1)
            html_source = driver.page_source
            # content = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(html_source, "html.parser")

            root_data = soup.find(class_='white-bg-box merchant-list')
            child_data = root_data.find_all("div")

            for child in child_data:
                if child['class'][0] == "row" and child['class'][1] == "merchant-search--item":
                    fact_location_informations = Fact_LocationInformations()
                    fact_location_informations.competitorId = locationSource.competitorId
                    fact_location_informations.timestamp = datetime.now()
                    fact_location_informations.latitude = child['data-latitude']
                    fact_location_informations.longitude = child['data-longitude']
                    fact_location_informations.postal_code = child['data-zip']
                    fact_location_informations.city = child['data-city']
                    fact_location_informations.street = child['data-street']
                    fact_location_informations.name = child['data-merchantname']
                    facts.append(fact_location_informations)

        return facts