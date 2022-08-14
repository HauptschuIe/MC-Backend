from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from HelperClasses.scraper import Scraper
from HelperClasses.fact_newsletter import Fact_Newsletter
import json
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

class NewsletterScraper(Scraper):
    def scrape_newsletter(self):
        facts = []
        options = wd.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")
        options.add_argument('log-level=3')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = wd.Chrome(ChromeDriverManager().install(), options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.get("https://www.gmx.net/?origin=lpc")
        driver.switch_to.default_content()
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="freemailLoginUsername"]').send_keys("letter.wettbewerbsanalyseWS21@gmx.de")
        driver.find_element(By.XPATH, '//*[@id="freemailLoginPassword"]').send_keys("An@lyseWS21")
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="freemailLoginForm"]/button').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/nav/nav-actions-menu/div[1]/div[1]/a[2]').click()
        time.sleep(3)
        elementframe3 = driver.find_element(By.XPATH, '//*[@id="thirdPartyFrame_mail"]')
        driver.switch_to.frame(elementframe3)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")
        mails = soup.find_all(class_="new")
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="checkbox-select-all"]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[1]/div[1]/div/form/div[2]/div[1]/ul[1]/li[2]/a').click()
        time.sleep(3)
        driver.find_element(By.XPATH,
                            '/html/body/div[6]/div/div[2]/ul/li[6]/input').click()
        for mail in mails:
            fact_newsletter = Fact_Newsletter()
            fact_newsletter.timestamp = datetime.now()
            fact_newsletter.body = ""
            if mail.find(class_="name") is not None:
                if mail.find(class_="name")['title'] !="":
                    if mail.find(class_="name")['title'].split()[0].replace('"','') == "MediaMarkt":
                        fact_newsletter.competitor_id = 3
                        fact_newsletter.title = mail.find(class_="subject").text.replace("'","")
                        if "Uhr" in mail.find(class_="date").text:
                            fact_newsletter.date = datetime.now()
                        else:
                            date_time_obj = datetime.strptime(mail.find(class_="date").text, '%d.%m.%Y')
                            fact_newsletter.date = date_time_obj
                        facts.append(fact_newsletter)
                    elif mail.find(class_="name")['title'].split()[0].replace('"','') == "SATURN":
                        fact_newsletter.competitor_id = 4
                        fact_newsletter.title = mail.find(class_="subject").text.replace("'","")
                        if "Uhr" in mail.find(class_="date").text:
                            fact_newsletter.date = datetime.now()
                        else:
                            date_time_obj = datetime.strptime(mail.find(class_="date").text, '%d.%m.%Y')
                            fact_newsletter.date = date_time_obj
                        facts.append(fact_newsletter)
                    elif mail.find(class_="name")['title'].split()[0].replace('"','') == "expert":
                        fact_newsletter.competitor_id = 6
                        fact_newsletter.title = mail.find(class_="subject").text.replace("'","")
                        if "Uhr" in mail.find(class_="date").text:
                            fact_newsletter.date = datetime.now()
                        else:
                            date_time_obj = datetime.strptime(mail.find(class_="date").text, '%d.%m.%Y')
                            fact_newsletter.date = date_time_obj
                        facts.append(fact_newsletter)
                else:
                    fact_newsletter.competitor_id = 5
                    print(mail.find(class_="subject"))
                    fact_newsletter.title = mail.find(class_="subject").text.replace("'","")
                    if "Uhr" in mail.find(class_="date").text:
                        fact_newsletter.date = datetime.now()
                    else:
                        date_time_obj = datetime.strptime(mail.find(class_="date").text, '%d.%m.%Y')
                        fact_newsletter.date = date_time_obj

                    facts.append(fact_newsletter)
        time.sleep(3)
        return facts