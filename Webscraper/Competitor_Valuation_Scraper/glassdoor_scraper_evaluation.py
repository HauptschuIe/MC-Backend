from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import transformkAToNull
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from HelperClasses.scraper import Scraper
from HelperClasses.fact_competitor_valuation import Fact_CompetitorValuation
from webdriver_manager.chrome import ChromeDriverManager
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



class GlassdoorScraperEvaluation(Scraper):
    def scrape_evaluation_details(self):
        facts = []
        for locationSource in self.dataSources:
            # Http Request
            options = wd.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument("start-maximized")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = wd.Chrome(ChromeDriverManager().install(),options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.53 Safari/537.36'})
            driver.get(locationSource.url)

            time.sleep(3)
            cookie_btn = driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
            submit_btn = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/article[2]/div[7]/main/div/div/div/div[1]/div[1]/div[3]/div/div/div[1]/div/div/span[2]').click()


            html_source = driver.page_source

            soup = BeautifulSoup(html_source, "html.parser")
            stars_chart = soup.find_all(class_= "col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum")
            donut_chart = soup.find_all(class_="donut__DonutStyle__donutchart_text_val")

            fact_competitor_valuation = Fact_CompetitorValuation()

            fact_competitor_valuation.competitor_id = locationSource.competitorId
            fact_competitor_valuation.timestamp = datetime.now()

            fact_competitor_valuation.total = stars_chart[0].text
            fact_competitor_valuation.culture_values = stars_chart[1].text
            fact_competitor_valuation.diversity_inclusion = stars_chart[2].text
            fact_competitor_valuation.work_life_balance = stars_chart[3].text
            fact_competitor_valuation.management_level = stars_chart[4].text
            fact_competitor_valuation.benefits = stars_chart[5].text
            fact_competitor_valuation.opportunities = stars_chart[6].text
            fact_competitor_valuation.recommendation = transformkAToNull(donut_chart[0].text)
            fact_competitor_valuation.commitment_gf = transformkAToNull(donut_chart[1].text)
            fact_competitor_valuation.pos_prognose = transformkAToNull(donut_chart[2].text)
            facts.append(fact_competitor_valuation)

        return facts


