from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import transformSplitStringSpace,removeStringTwoChar,removeStringLastChar,removeStringFirstChar,replacePoint,transformStringToFLoat
from HelperClasses.scraper import Scraper
from HelperClasses.fact_customer_review import Fact_CustomerReview

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



class TrustpilotScraper(Scraper):
    def scrape_customer_review(self):
        facts = []
        for locationSource in self.dataSources:

            # Http Request
            content = requests.get(locationSource.url, headers=headers)
            soup = BeautifulSoup(content.text, "html.parser")

            # Scrape valuation Informations
            valuation_all = soup.find_all(class_='typography_typography__QgicV typography_bodysmall__irytL typography_color-gray-7__9Ut3K typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3 styles_cell__qnPHy styles_percentageCell__cHAnb')
            valuation_total = soup.select("div.styles_rating__NPyeH > p")
            valuation_total_description_reviews = soup.find(class_="typography_typography__QgicV typography_bodysmall__irytL typography_color-gray-7__9Ut3K typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3 styles_text__W4hWi")

            fact_customer_review = Fact_CustomerReview()

            fact_customer_review.competitor_id = locationSource.competitorId

            fact_customer_review.timestamp = datetime.now()

            if valuation_total is not None:
                fact_customer_review.total = transformStringToFLoat(valuation_total[0].text)

            if valuation_total_description_reviews is not None:
                parts = transformSplitStringSpace(valuation_total_description_reviews.text)
                fact_customer_review.total_reviews = replacePoint(removeStringLastChar(parts[0]))
                fact_customer_review.total_description = removeStringFirstChar(parts[-1])

            if valuation_all is not None:
                fact_customer_review.excellent = removeStringTwoChar(valuation_all[0].text)
                fact_customer_review.good = removeStringTwoChar(valuation_all[1].text)
                fact_customer_review.acceptable = removeStringTwoChar(valuation_all[2].text)
                fact_customer_review.deficient = removeStringTwoChar(valuation_all[3].text)
                fact_customer_review.insufficient = removeStringTwoChar(valuation_all[4].text)
            facts.append(fact_customer_review)
        return facts

