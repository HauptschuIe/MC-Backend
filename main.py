import os
from Webscraper.Similarweb.visitors_informations import *
from Webscraper.Price_Availability_Scraper.amazon_price import *
from Webscraper.Price_Availability_Scraper.euronics_price import *
from Webscraper.Price_Availability_Scraper.expert_price import *
from Webscraper.Price_Availability_Scraper.mediamarkt_price import *
from Webscraper.Price_Availability_Scraper.otto_price import *
from Webscraper.Price_Availability_Scraper.saturn_price import *
from Webscraper.Social_Media_Scraper.youtube_channel_data import scrape_youtube_channel_data
from Webscraper.Social_Media_Scraper.twitter_account_data import scrape_twitter_account_data
from Webscraper.Social_Media_Scraper.twitter_mentions_data import scrape_twitter_mentions_data
from Webscraper.Social_Media_Scraper.twitter_tweets_data import scrape_twitter_tweet_data
from Webscraper.googleTrends import *
from Webscraper.Locations_Scraper.euronics_locations import *
from Webscraper.Locations_Scraper.mediamarkt_locations import *
from Webscraper.Locations_Scraper.saturn_locations import *
from Webscraper.Locations_Scraper.expert_locations import *
from Webscraper.Competitor_Valuation_Scraper.glassdoor_scraper_evaluation import *
from Webscraper.Competitor_Valuation_Scraper.glassdoor_scraper_interview import *
from Webscraper.trustpilot_customer_review.trustpilot_scraper_valuation import *
from Webscraper.trustpilot_customer_review.trustpilot_scraper_evaluation import *
from Webscraper.Newsletter_Scraper.newsletter_data import *
from Webscraper.Newsletter_Scraper.newsletter_wordcount import *
from Webscraper.Newsletter_Scraper.newsletter_wordcloud import *

from datetime import datetime,date
import logging
import logging.handlers
import traceback

os.environ['WDM_LOG'] = "false"

if __name__ == "__main__":

    print(f"Running script at {datetime.now()}")

    notiFromaddr = "letter.wettbewerbsanalyseWS21@gmx.de"
    notiToaddr = ["WettbewerbsanalyseWS21.hsrt@gmail.com"]
    notiSubj = "Management Cockpit Scraper error!"
    notiCredentials = ("letter.wettbewerbsanalyseWS21@gmx.de", "An@lyseWS21")

    smtp_handler = logging.handlers.SMTPHandler(mailhost=("mail.gmx.net", 587),
                                            fromaddr=notiFromaddr, 
                                            toaddrs=notiToaddr,
                                            subject=notiSubj,
                                            credentials=notiCredentials,
                                            secure=())

    logger = logging.getLogger()
    logger.addHandler(smtp_handler)
    logging.getLogger('WDM').setLevel(logging.NOTSET)



    #############################################################
    ##################### MONTHLY SCRAPERS ######################
    #############################################################
    today = date.today()
    if(today.day == 11):
        print("Day of the month: ", today.day, " -> running monthly scrapers")
        ################ FT_VISITORS, FT_MARKETING_CHANNELS, FT_TRAFFIC_KEYWORDS
        try:
            scraper_SimilarWeb = Scraper_SimilarWeb("1", "DummyDescription", getDataSourcesCompetitorRelatedForScraper("1"))

            #returns a tuple of facts; first tuple is visitors, second is marketing_channels and third is keywords
            facts = scraper_SimilarWeb.scrape()

            insertFacts_SimilarWeb_Visitor(facts[0])
            insertFacts_SimilarWeb_Marketing_Channels(facts[1])
            insertFacts_SimilarWeb_Keywords(facts[2])
            insertFacts_SimilarWeb_Zielgruppendemografie(facts[3])


        except Exception as visitors_error:
            print("Exception while trying to update FT_VISITORS, FT_MARKETING_CHANNELS & FT_TRAFFIC_KEYWORDS")
            logging.error(traceback.format_exc())
            logger.exception('Exception while trying to update FT_VISITORS, FT_MARKETING_CHANNELS & FT_TRAFFIC_KEYWORDS')


        ################ FT_LOCATION_INFORMATIONS
        ### Euronics Locations
        try:
            EuronicsLocationsScraper = EuronicsLocationsScraper("2", "DummyDescription",getLocationSourcesCompetitorRelatedForScraper("2", "5"))
            insertFacts_LocationsInformations(EuronicsLocationsScraper.scrape_location_details())
            print("EuronicsLocationsScraper success")
        except Exception as euronics_location_scraper_error:
            print("Exception in Euronics Location Scraper")
            logging.error(traceback.format_exc())
            logger.exception('Exception in Euronics Location Scraper')

        ### MediaMarkt Locations
        try:
            MediaMarktLocationsScraper = MediaMarktLocationsScraper("2", "DummyDescription",
                                                                    getLocationSourcesCompetitorRelatedForScraper("2", "3"))
            insertFacts_LocationsInformations(MediaMarktLocationsScraper.scrape_location_details())
            print("MediaMarktLocationsScraper success")
        except Exception as mediamarkt_location_scraper_error:
            print("Exception in Media Markt Location Scraper")
            logging.error(traceback.format_exc())
            logger.exception('Exception in Media Markt Location Scraper')

        ### Saturn Locations
        try:
            SaturnLocationsScraper = SaturnLocationsScraper("2", "DummyDescription",
                                                                    getLocationSourcesCompetitorRelatedForScraper("2", "4"))
            insertFacts_LocationsInformations(SaturnLocationsScraper.scrape_location_details())
            print("SaturnLocationsScraper success")
        except Exception as saturn_location_scraper_error:
            print("Exception in Saturn Location Scraper")
            logging.error(traceback.format_exc())
            logger.exception('Exception in Saturn Location Scraper')

        ### Expert Locations
        try:
            ExpertLocationsScraper = ExpertLocationsScraper("2", "DummyDescription",
                                                                    getLocationSourcesCompetitorRelatedForScraper("2", "6"))
            insertFacts_LocationsInformations(ExpertLocationsScraper.scrape_location_details())
            print("ExpertLocationsScraper success")
        except Exception as expert_location_scraper_error:
            print("Exception in Expert Location Scraper")
            logging.error(traceback.format_exc())
            logger.exception('Exception in Expert Location Scraper')
    else:
        print("Day of the month: ", today.day, " -> NOT running monthly scrapers")

    #############################################################
    ##################### DAILIY SCRAPERS #######################
    #############################################################

    ################ FT_CUSTOEMR_REVIEW
     ### Trustpilot Customer Review Per Source
    try:
        TrustpilotScraperPerSource = TrustpilotScraperPerSource("7", "DummyDescription",
                                                        getDataSourcesCompetitorRelatedForScraper("7"))

        insertFacts_CustomerReviewSourceNew(TrustpilotScraperPerSource.scrape_customer_review_source())
        print("TrustpilotScraperPerSource success")
    except Exception as trustpilot_customerreview_per_source_scraper_error:
        print("Exception in Trustpilot Customer Review Per Source Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Trustpilot Customer Review Per Source Scraper')
        
    ### Trustpilot Customer Review
    try:
        TrustpilotScraper = TrustpilotScraper("6", "DummyDescription",
                                                        getDataSourcesCompetitorRelatedForScraper("6"))
        insertFacts_CustomerReview(TrustpilotScraper.scrape_customer_review())
        print("TrustpilotScraper success")
    except Exception as trustpilot_customerreview_scraper_error:
        print("Exception in Trustpilot Customer Review Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Trustpilot Customer Review Scraper')
    
    ################ FT_COMPETITOR_INTERVIEW
    ### CompetitorInterview Glassdoor
    try:
        GlassdoorScraperInterview = GlassdoorScraperInterview("5", "DummyDescription",
                                                        getDataSourcesCompetitorRelatedForScraper("5"))
        insertFacts_CompetitorInterview(GlassdoorScraperInterview.scrape_interview_details())
        print("GlassdoorScraperInterview success")
    except Exception as expert_competitorinterview_scraper_error:
        print("Exception in CompetitorInterview Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in CompetitorInterview Scraper')
    
    ################ FT_COMPETITOR_VALUATION
    ### CompetitorValuation Glassdoor
    try:
        GlassdoorScraperEvaluation = GlassdoorScraperEvaluation("4", "DummyDescription",
                                                        getDataSourcesCompetitorRelatedForScraper("4"))
        insertFacts_CompetitorValuation(GlassdoorScraperEvaluation.scrape_evaluation_details())
        print("GlassdoorScraperEvaluation success")
    except Exception as expert_competitorvaluation_scraper_error:
        print("Exception in CompetitorValuation Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in CompetitorValuation Scraper')

    ################ FT_PRODUCT_INFORMATIONS
    ### Amazon
    try:
        AmazonProductScraper = AmazonProductScraper("3", "DummyDescription",getProductSourcesCompetitorRelatedForScraper("3","1"))
        insertFacts_ProductInformations(AmazonProductScraper.scrape_product_details())
        print("AmazonProductScraper success")
    except Exception as amazon_product_scraper_error:
        print("Exception in Amazon Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Amazon Scraper')
    ### Otto
    try:
        OttoProductScraper = OttoProductScraper("3", "DummyDescription",getProductSourcesCompetitorRelatedForScraper("3", "2"))
        insertFacts_ProductInformations(OttoProductScraper.scrape_product_details())
        print("OttoProductScraper success")
    except Exception as otto_product_scraper_error:
        print("Exception in Otto Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Otto Scraper')
    ### Media Markt
    try:
        MediaMarktProductScraper = MediaMarktProductScraper("3", "DummyDescription",getProductSourcesCompetitorRelatedForScraper("3", "3"))
        insertFacts_ProductInformations(MediaMarktProductScraper.scrape_product_details())
        print("MediaMarktProductScraper success")
    except Exception as mediamarkt_product_scraper_error:
        print("Exception in Media Markt Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Media Markt Scraper')
    ### Saturn
    try:
        SaturnProductScraper = SaturnProductScraper("3", "DummyDescription",getProductSourcesCompetitorRelatedForScraper("3", "4"))
        insertFacts_ProductInformations(SaturnProductScraper.scrape_product_details())
        print("SaturnProductScraper success")
    except Exception as saturn_product_scraper_error:
        print("Exception in Saturn Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Saturn Scraper')
    ### Euronics
    try:
        EuronicsProductScraper = EuronicsProductScraper("3", "DummyDescription",getProductSourcesCompetitorRelatedForScraper("3", "5"))
        insertFacts_ProductInformations(EuronicsProductScraper.scrape_product_details())
        print("EuronicsProductScraper success")
    except Exception as euronics_product_scraper_error:
        print("Exception in Euronics Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Euronics Scraper')
    ### Expert
    try:
        ExpertProductScraper = ExpertProductScraper("3", "DummyDescription",getProductSourcesCompetitorRelatedForScraper("3", "6"))
        insertFacts_ProductInformations(ExpertProductScraper.scrape_product_details())
        print("ExpertProductScraper success")
    except Exception as expert_product_scraper_error:
        print("Exception in Expert Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Expert Scraper')

    ################ FT_SHOPPING_POPULARITY
    try:
        updateFacts_ShoppingPopularity_LatestToFalse()
        #requests are done product by product -> one must not compare the results between different products!!
        for product in getProducts():
            try:
                #Attention: this will only work up to five competitors in the table! Trends does only accept a maximum of five parameters!!
                scraper_GoogleTrends = Scraper_GoogleTrends("8", "DummyDescription", getDataSourcesProductRelatedByProductIdForScraper("8", str(product.id)))
                insertFacts_ShoppingPopularity(scraper_GoogleTrends.scrape())
            except (pytrends.exceptions.ResponseError) as error:
                print("error while performing googleTrends request for product_id:  " + str(product.id) + ". Check if url in dt_product_source exists.")
            except (KeyError) as error2:
                print("could not find google trends results for product_id: " + str(product.id))
    except Exception as shopping_popularity_error:
        print("Exception while trying to update FT_SHOPPING_POPULARITY")
        logging.error(traceback.format_exc())
        logger.exception('Exception while trying to update FT_SHOPPING_POPULARITY')

    ################ FT_YOUTUBE_CHANNEL_DATA
    try:
        scrape_youtube_channel_data()
        print("Youtube Channel Data success")
    except Exception as youtube_error:
        print("Exception while trying to update youtube facts")
        logging.error(traceback.format_exc())
        logger.exception('Exception while trying to update youtube facts')
    
    ################ FT_TWITTER_ACCOUNT_DATA
    try:
        scrape_twitter_account_data()
        print("Twitter account data success")
    except Exception as twitter_error:
        print("Exception while trying to update twitter facts")
        logging.error(traceback.format_exc())
        logger.exception('Exception while trying to update twitter facts')

    ################ FT_TWITTER_COMMENTS_DATA
    try: 
        scrape_twitter_mentions_data()
        print("Twitter mentions data success")
    except Exception as twitter_error:
        print("Exception while trying to update twitter comments")
        logging.error(traceback.format_exc())
        logger.exception('Exception while trying to update twitter comments')
    
    ################ FT_NEWSLETTER
    ### Newsletter
    try:
        NewsletterScraper = NewsletterScraper("4", "DummyDescription","https://www.gmx.net/")
        insertFacts_Newsletter(NewsletterScraper.scrape_newsletter())
        print("Newsletter Scraper success")
    except Exception as expert_competitorvaluation_scraper_error:
        print("Exception in Newsletter Scraper")
        logging.error(traceback.format_exc())
        logger.exception('Exception in Newletter Scraper')

    ################ FT_NEWSLETTERWORDS
    ### NewsletterWords
    try:
        NewsletterWordcount = NewsletterWordcount()
        insertFacts_NewsletterWords(NewsletterWordcount.wordcount_newsletter())
        print("Newsletter Wordcount success")
    except Exception as expert_competitorvaluation_scraper_error:
        print("Exception in Newsletter Wordcount")
        logging.error(traceback.format_exc())
        #logger.exception('Exception in Newletter Wordcount')


    ################ FT_NEWSLETTERWORDCLOUD
    ### NewsletterWordcloud
    try:
        NewsletterWordcloud = NewsletterWordcloud()
        insertFacts_NewsletterWordcloud(NewsletterWordcloud.wordcloud_newsletter())
        print("Newsletter Wordcloud success")
    except Exception as expert_competitorvaluation_scraper_error:
        print("Exception in Newsletter Wordcloud")
        logging.error(traceback.format_exc())
        #logger.exception('Exception in Newletter Wordcount')
    

    ################ FT_TWITTER_TWEET_DATA
    try: 
        scrape_twitter_tweet_data()
        print("Twitter tweet data success")
    except Exception as twitter_error:
        print("Exception while trying to update twitter tweets")
        logging.error(traceback.format_exc())
        logger.exception('Exception while trying to update twitter tweets')

