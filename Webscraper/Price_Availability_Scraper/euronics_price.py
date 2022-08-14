from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import transformPriceToFloatEuronics
from selenium import webdriver as wd
from webdriver_manager.chrome import ChromeDriverManager
import time
from HelperClasses.scraper import Scraper
from HelperClasses.fact_product_informations import Fact_ProductInformations

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


class EuronicsProductScraper(Scraper):

    def scrape_product_details(self):
        facts = []
        for productSource in self.dataSources:
            # Http Request
            chrome_options = wd.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('log-level=3')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = wd.Chrome(ChromeDriverManager().install(),options=chrome_options)
            driver.get(productSource.url)
            time.sleep(1)
            html_source = driver.page_source

            #content = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(html_source, "html.parser")

            fact_product_informations = Fact_ProductInformations()
            fact_product_informations.competitorId = productSource.competitorId
            fact_product_informations.productId = productSource.productId
            fact_product_informations.timestamp = datetime.now()

            availibility = soup.find_all(class_='delivery--text delivery--text-available')

            if len(availibility)>1:
                fact_product_informations.availability_status_id = self.checkAvailability(availibility[1].text)
            else:
                fact_product_informations.availability_status_id = 2


            fact_product_informations.price = soup.find(id='product-price')
            if soup.find(class_='content--discount') is None:
                fact_product_informations.price_status_id = 1
            else:
                fact_product_informations.price_status_id = 2

            if fact_product_informations.price is not None:
                fact_product_informations.price = fact_product_informations.price.text

            fact_product_informations.price = transformPriceToFloatEuronics(fact_product_informations.price)
            
            if fact_product_informations.price == None:
                fact_product_informations.price = "Null"
            
            facts.append(fact_product_informations)
        return facts

    def checkAvailability(self, root_availability):
        if "sofort" in root_availability or "Versandbereit" in root_availability or "auf Lager" in root_availability:
            verfuegbarkeit = str(1)
        else:
            verfuegbarkeit = str(2)

        return verfuegbarkeit