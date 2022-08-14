from Webscraper.Similarweb.visitors_informations import *
import logging
import traceback
from datetime import datetime

if __name__ == "__main__":
    print(f"Running script at {datetime.now()}")

    ################ FT_VISITORS, FT_MARKETING_CHANNELS, FT_TRAFFIC_KEYWORDS
    try:
        scraper_SimilarWeb = Scraper_SimilarWeb("1", "DummyDescription", getDataSourcesCompetitorRelatedForScraper("1"))

        #returns a tuple of facts; first tuple is visitors, second is marketing_channels and third is keywords
        facts = scraper_SimilarWeb.scrape()

        insertFacts_SimilarWeb_Visitor(facts[0])
        insertFacts_SimilarWeb_Marketing_Channels(facts[1])
        insertFacts_SimilarWeb_Keywords(facts[2])

    except Exception as visitors_error:
        print("Exception while trying to update FT_VISITORS, FT_MARKETING_CHANNELS & FT_TRAFFIC_KEYWORDS")
        logging.error(traceback.format_exc())