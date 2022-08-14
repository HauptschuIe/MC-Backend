from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import transformPriceToFloat
from selenium import webdriver as wd
from webdriver_manager.chrome import ChromeDriverManager
import time
from HelperClasses.scraper import Scraper
from HelperClasses.fact_product_informations import Fact_ProductInformations

# Initialize Header Information
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.132 Safari/537.36'
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8," \
         "application/signed-exchange;v=b3;q=0.9 "
accept_en = "gzip, deflate, sdch, br"
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


class ExpertProductScraper(Scraper):

    def scrape_product_details(self):
        facts = []
        for productSource in self.dataSources:
            # Http Request
            options = wd.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('log-level=3')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = wd.Chrome(ChromeDriverManager().install(),options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.53 Safari/537.36'})
            driver.get(productSource.url)
            time.sleep(1)
            html_source = driver.page_source

            soup = BeautifulSoup(html_source, "html.parser")

            fact_product_informations = Fact_ProductInformations()
            fact_product_informations.competitorId = productSource.competitorId
            fact_product_informations.productId = productSource.productId
            fact_product_informations.timestamp = datetime.now()

            product_available = self.isProductAvailable(soup.find(class_='widget widget-Text '
                                                                         'widget-Text---c643eae2-bf63-4f6b-8975'
                                                                         '-4c2342b06cf3 widget-Text---view-text '
                                                                         'widget-Text---preset-default margin-xs-top-70 '
                                                                         'margin-lg-top-0  '))
            if product_available:
                if soup.find('span', class_="widget-ArticleStatus-statusPointText") is not None:
                    if self.isProductOnlineAvailable(soup.find('span', class_="widget-ArticleStatus-statusPointText").text):
                        fact_product_informations.availability_status_id = 1
                        fact_product_informations.price = soup.find(class_="widget-ArticlePrice-price").text
                        if soup.find(class_="widget-FormerPrice-percentage-text") is None:
                            fact_product_informations.price_status_id = 1
                        else:
                            fact_product_informations.price_status_id = 2
                    else:
                        fact_product_informations.availability_status_id = 2
                        fact_product_informations.price = "Null"
                        fact_product_informations.price_status_id = 3
                else:
                    fact_product_informations.availability_status_id = 2
                    fact_product_informations.price = "Null"
                    fact_product_informations.price_status_id = 3
            else:
                fact_product_informations.price_status_id = 3
                fact_product_informations.availability_status_id = 2
                fact_product_informations.price = "Null"

            if fact_product_informations.price != "Null":
                fact_product_informations.price = transformPriceToFloat(fact_product_informations.price)

            facts.append(fact_product_informations)
        return facts

    def isProductOnlineAvailable(self, productRootOnline):
        if "Online auf Lager" in productRootOnline:
            return True
        else:
            return False

    def isProductAvailable(self, productRoot):
        if productRoot is None:
            return True
        else:
            return False
