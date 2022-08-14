import requests
from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import transformPriceToFloat
import json
from HelperClasses.scraper import Scraper
from HelperClasses.fact_product_informations import Fact_ProductInformations

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
           'accept-encoding': accept_en,
           'accept-language': accept_lan,
           'cache-control': cache_con,
           'cache': cokies,
           'user-agent': user_agent, }


class OttoProductScraper(Scraper):

    def scrape_product_details(self):
        facts = []
        for productSource in self.dataSources:
            # Http Request
            content = requests.get(productSource.url, headers=headers)
            soup = BeautifulSoup(content.text, "html.parser")

            fact_product_informations = Fact_ProductInformations()
            fact_product_informations.competitorId = productSource.competitorId
            fact_product_informations.productId = productSource.productId
            fact_product_informations.timestamp = datetime.now()

            # Scrape availability: variation_id: allows to check availability of product
            variation_id = soup.find(class_='js_metaVariationId')
            variation_id = variation_id.find_all("meta")[1]['content']
            data = json.loads(soup.find('script', id='productDataJson').string)
            if data['variations'][variation_id]['availability']['status'] == "delayed":
                fact_product_informations.availability_status_id = 2
            else:
                fact_product_informations.availability_status_id = 1

            # Scrape Price: product_Price: price of product
            fact_product_informations.price = soup.find(id='normalPriceAmount')
            if fact_product_informations.price is None:
                fact_product_informations.price = soup.find(id='reducedPriceAmount').text
                fact_product_informations.price_status_id = 2
            else:
                fact_product_informations.price = fact_product_informations.price.text
                fact_product_informations.price_status_id = 1

            fact_product_informations.price = transformPriceToFloat(fact_product_informations.price)

            facts.append(fact_product_informations)
        return facts
