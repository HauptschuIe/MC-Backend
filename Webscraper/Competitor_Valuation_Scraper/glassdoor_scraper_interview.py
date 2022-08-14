from bs4 import BeautifulSoup
from datetime import datetime
from DataTransformation.transformation import removeStringLastChar, transformStringToFLoat
from HelperClasses.scraper import Scraper
from HelperClasses.fact_competitor_interview import Fact_CompetitorInterview
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
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

class GlassdoorScraperInterview(Scraper):

    def scrape_interview_details(self):
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
            print(locationSource.url)
            time.sleep(3)

            cookie_btn = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

            try:
                mehr_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/article[2]/div[5]/main/div/div[1]/div[1]/div[3]/div/div/div[2]/div[2]/button').click()
            except:
                print("no extra data")

            html_source = driver.page_source

            soup = BeautifulSoup(html_source, "html.parser")
            interview_label = soup.find_all(class_="mr-xxsm")
            interview_value = soup.find_all(class_="ml-auto")


            fact_competitor_interview = Fact_CompetitorInterview()

            fact_competitor_interview.competitor_id = locationSource.competitorId
            fact_competitor_interview.timestamp = datetime.now()

            fact_competitor_interview.difficulty = transformStringToFLoat(soup.find(class_="css-155sv15 es3tan90").text)

            for index, child in enumerate(interview_value):
                if interview_label[index].text == "Positiv":
                    fact_competitor_interview.positiv = removeStringLastChar(child.text)
                elif interview_label[index].text == "Negativ":
                    fact_competitor_interview.negativ = removeStringLastChar(child.text)
                elif interview_label[index].text == "Neutral":
                    fact_competitor_interview.neutral = removeStringLastChar(child.text)
                elif interview_label[index].text == "Online-Bewerbung":
                    fact_competitor_interview.online = removeStringLastChar(child.text)
                elif interview_label[index].text == "Personalvermittler":
                    fact_competitor_interview.recruiter = removeStringLastChar(child.text)
                elif interview_label[index].text == "Empfehlung":
                    fact_competitor_interview.recommendation = removeStringLastChar(child.text)
                elif interview_label[index].text == "Hochschul-Recruiting":
                    fact_competitor_interview.university_recruiter = removeStringLastChar(child.text)
                elif interview_label[index].text == "Persönlich":
                    fact_competitor_interview.personal = removeStringLastChar(child.text)
                elif interview_label[index].text == "Andere":
                    fact_competitor_interview.other = removeStringLastChar(child.text)
                elif interview_label[index].text == "Vermittlungsagentur":
                    fact_competitor_interview.agency = removeStringLastChar(child.text)
            facts.append(fact_competitor_interview)


        return facts
