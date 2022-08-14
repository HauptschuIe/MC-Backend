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


class MediaMarktProductScraper(Scraper):

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
            time.sleep(2)
            html_source = driver.page_source

            # content = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(html_source, "html.parser")

            fact_product_informations = Fact_ProductInformations()
            fact_product_informations.competitorId = productSource.competitorId
            fact_product_informations.productId = productSource.productId
            fact_product_informations.timestamp = datetime.now()

            # Scrape Price: product_Price: price of product
            check_price_status = soup.find(class_="StyledBrandedStrikePrice-sc-1stgwju-2 kDeCRX")
            if check_price_status is not None:
                fact_product_informations.price = soup.find(
                    class_='WholePrice-sc-1r6586o-7').text
                if soup.find(
                        class_='DecimalPrice-sc-1r6586o-8').text != "":
                    fact_product_informations.price = fact_product_informations.price + str(soup.find(
                        class_='DecimalPrice-sc-1r6586o-8').text)
                fact_product_informations.price_status_id = 2
            else:
                fact_product_informations.price = soup.find_all(class_='ScreenreaderTextSpan-sc-11hj9ix-0 kZCfsu')[
                    0].text
                fact_product_informations.price_status_id = 1

            # Scrape availability: availability: allows to check availability of product
            availability = soup.find(class_='StyledAvailabilityStatusWrapper-sc-901vi5-3 jbEToP')
            availability = availability.find("span")['class'][1]
            fact_product_informations.availability_status_id = self.check_availability(availability)

            fact_product_informations.price = transformPriceToFloat(fact_product_informations.price)
            facts.append(fact_product_informations)
        return facts

    def check_availability(self, root_vailability):
        if "gxSFkJ" in root_vailability or "gDZArI" in root_vailability:
            verfuegbarkeit = str(1)
        else:
            verfuegbarkeit = str(2)

        return verfuegbarkeit
