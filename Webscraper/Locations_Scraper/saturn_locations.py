import requests
from bs4 import BeautifulSoup
from geopy import geocoders
from geopy.geocoders import Nominatim
import urllib3
from datetime import datetime
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


class SaturnLocationsScraper(Scraper):

    def scrape_location_details(self):
        facts = []
        self.urls = []
        for locationSource in self.dataSources:
            geolocator = Nominatim(user_agent="Wettbewerbszahlen")

            # HTTP Request
            content = requests.get(locationSource.url, headers=headers)
            soup = BeautifulSoup(content.text, features="html.parser")

            root_urls = soup.find('section', class_='StyledSection-hamlz2-0 eauyDa')
            children_urls = root_urls.findChildren('a')
            for child in children_urls:
                self.urls.append("https://www.saturn.de"+str(child['href']))
            counter = 0

            for child in self.urls:
                counter+= 1

                contentStore = requests.get(child, headers=headers)
                soup = BeautifulSoup(contentStore.text, features="html.parser")

                fact_location_informations = Fact_LocationInformations()
                fact_location_informations.competitorId = locationSource.competitorId
                fact_location_informations.timestamp = datetime.now()

                locations = soup.find_all(class_="BaseTypo-sc-1jga2g7-0 izkVco StyledInfoTypo-sc-1jga2g7-1 hDReip")

                fact_location_informations.name = locations[0].text
                fact_location_informations.street  = locations[1].text
                informations = locations[2].text.split(" ", 1)
                fact_location_informations.postal_code = informations[0]
                fact_location_informations.city = informations[1]

                location = geolocator.geocode(fact_location_informations.postal_code +" " +fact_location_informations.city+" "+fact_location_informations.street)
                if location is not None:
                    fact_location_informations.latitude = location.latitude
                    fact_location_informations.longitude = location.longitude
                else:
                    location = geolocator.geocode(fact_location_informations.city + " Deutschland")
                    if location is not None:
                        fact_location_informations.latitude = location.latitude
                        fact_location_informations.longitude = location.longitude
                    else:
                        location = geolocator.geocode(fact_location_informations.street + " " + fact_location_informations.postal_code)
                        if location is not None:
                            fact_location_informations.latitude = location.latitude
                            fact_location_informations.longitude = location.longitude
                facts.append(fact_location_informations)

        return facts