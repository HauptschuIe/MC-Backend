import requests
from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import transformPriceToFloat
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


class AmazonProductScraper(Scraper):

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

            # Scrape Price: product_Price: price of product
            parent_price = soup.find('span', class_='a-price a-text-price a-size-medium apexPriceToPay')
            if parent_price is None:
                sonderpreis = soup.find(id='priceblock_ourprice')
                if sonderpreis is None:
                    lastchance = soup.find('span', class_='a-offscreen')
                    if lastchance is None:
                        fact_product_informations.price = "Null"
                    else:
                        if '€' in lastchance.text:
                            fact_product_informations.price = lastchance.text
                        else:
                            fact_product_informations.price = "Null"
                else:
                    fact_product_informations.price = sonderpreis.text
            else:
                fact_product_informations.price = parent_price.findChildren('span', class_='a-offscreen')[0].text

            root_price = soup.find_all('td', class_='a-color-secondary a-size-base a-text-right a-nowrap')
            if len(root_price) > 2:
                fact_product_informations.price_status_id =str(2)
            elif fact_product_informations.price_status_id == "Null":
                fact_product_informations.price_status_id = str(3)
            else:
                fact_product_informations.price_status_id = str(1)

            availability = soup.find(id='availability')
            availability = availability.find("span")
            if availability != None:
                availability = availability['class'][1]
            else:
                availability = ""

            fact_product_informations.availability_status_id = self.check_availability(availability,fact_product_informations.price)

            if fact_product_informations.price != "Null":
                fact_product_informations.price = transformPriceToFloat(fact_product_informations.price)

            facts.append(fact_product_informations)

        return facts

    def check_availability(self, root_vailability,price):
        if "a-color-success" in root_vailability or "a-color-price" in root_vailability:
            if price != "Null":
                verfuegbarkeit = str(1)
            else:
                verfuegbarkeit = str(2)
        else:
            verfuegbarkeit = str(2)
        return verfuegbarkeit