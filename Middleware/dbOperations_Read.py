import datetime
import psycopg2
import requests
from HelperClasses.competitor import Competitor
from HelperClasses.product import Product
from HelperClasses.data_source_competitorRelated import Data_Source_CompetitorRelated
from HelperClasses.data_source_productRelated import Data_Source_ProductRelated
from HelperClasses.proxy import ScraperProxy
from Middleware.config import config

def getCompetitorById(id):
    # TODO: DB query to pull competitor by id; init & return Competitor object
    return None

# DB query to pull all competitors; return list of competitor objects
def getCompetitors():

    connection = None
    competitors = []

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        #print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute(
            "SELECT competitor_id, name")
        sqlResult = cursor.fetchall()

        #print("Print each row and it's columns values")
        for row in sqlResult:
            # TODO: include abbreviation in select and instantiation
            competitor = Competitor()
            competitor.id = row[0]
            competitor.description = row[1]
            competitors.append(competitor)

        return competitors

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not pull competitors from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

def getProductSourcesCompetitorRelatedForScraper(scraperId,competitorId):
    connection = None
    ProductSourcesCompetitorRelatedForScraper = []

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute("SELECT ps.id, ps.competitor_id, ps.product_id, ps.url, ps.scraper_id FROM dt_product_sources ps, dt_products p WHERE ps.scraper_id = " + str(
                scraperId) + " AND ps.product_id = "
                              "p.id AND ps.competitor_id = " + str(
                competitorId) + " AND p.active = true ORDER BY ps.product_id")
        sqlResult = cursor.fetchall()

        # print("Print each row and it's columns values")
        for row in sqlResult:
            data_Source_productRelated = Data_Source_ProductRelated()
            data_Source_productRelated.id = row[0]
            data_Source_productRelated.competitorId = row[1]
            data_Source_productRelated.productId = row[2]
            data_Source_productRelated.url = row[3]
            data_Source_productRelated.scraperId = row[4]
            ProductSourcesCompetitorRelatedForScraper.append(data_Source_productRelated)

        return ProductSourcesCompetitorRelatedForScraper

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not pull dataSourcesCompetitorRelatedForScraper from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")

def getDataSourcesCompetitorRelatedForScraper(scraperId):
    
    connection = None
    dataSourcesCompetitorRelatedForScraper = []

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        #print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute(
            "SELECT id, competitor_id, url, scraper_id FROM dt_competitor_sources WHERE scraper_id = " + str(scraperId))
        sqlResult = cursor.fetchall()

        #print("Print each row and it's columns values")
        for row in sqlResult:
            data_Source_CompetitorRelated = Data_Source_CompetitorRelated()
            data_Source_CompetitorRelated.id = row[0]
            data_Source_CompetitorRelated.competitorId = row[1]
            data_Source_CompetitorRelated.url = row[2]
            data_Source_CompetitorRelated.scraperId = row[3]
            dataSourcesCompetitorRelatedForScraper.append(data_Source_CompetitorRelated)

        return dataSourcesCompetitorRelatedForScraper

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not pull dataSourcesCompetitorRelatedForScraper from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

#Method still under construction
def getDataSourcesProductRelatedByProductIdForScraper(scraperId, productId):
    
    connection = None
    dataSourcesProductRelatedForScraper = []

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        #print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        
        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute(
            "SELECT id, competitor_id, product_id, url, scraper_id FROM dt_product_sources WHERE scraper_id = " + str(scraperId) + " AND product_id = " + str(productId))
        sqlResult = cursor.fetchall()

        #print("Print each row and it's columns values")
        for row in sqlResult:
            data_Source_ProductRelated = Data_Source_ProductRelated()
            data_Source_ProductRelated.id = row[0]
            data_Source_ProductRelated.competitorId = row[1]
            data_Source_ProductRelated.productId = row[2]
            data_Source_ProductRelated.url = row[3]
            data_Source_ProductRelated.scraperId = row[4]
            dataSourcesProductRelatedForScraper.append(data_Source_ProductRelated)

        return dataSourcesProductRelatedForScraper

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not pull dataSourcesProductRelatedForScraper from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# DB query to pull all Products; return list of product objects
def getProducts():

    connection = None
    products = []

    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute(
            "SELECT id, description,  category_id, active FROM dt_products")
        sqlResult = cursor.fetchall()

        #print("Print each row and it's columns values")
        for row in sqlResult:
            product = Product()
            product.id = row[0]
            product.description = row[1]
            product.categoryId = row[2]
            product.active = row[3]
            products.append(product)

        return products

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not pull competitors from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

def getActiveProxiesForScraper(scraperId):
    
    connection = None
    proxies = []

    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute(
            "SELECT id, address,  scraper_Id, date_last_used, active FROM dt_proxies WHERE scraper_Id = " + str(scraperId) + "AND active = 'TRUE'")
        sqlResult = cursor.fetchall()

        #print("Print each row and it's columns values")
        for row in sqlResult:
            sprox = ScraperProxy()
            sprox.id = row[0]
            sprox.address = row[1]
            sprox.scraperId = row[2]
            sprox.dateLastUsed = row[3]
            sprox.active = row[4]
            proxies.append(sprox)

        return proxies

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL. ", error)
        # TODO: define specific exception
        raise Exception("Could not pull proxies from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")
            
def getLocationSourcesCompetitorRelatedForScraper(scraper_id,competitor_id):
    connection = None
    dataSourcesCompetitorRelatedForScraper = []

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime

        cursor.execute("SELECT id, competitor_id, url, scraper_id FROM dt_competitor_sources cs WHERE cs.scraper_id = " + str(scraper_id) + " AND cs.competitor_id = " + str(competitor_id))
        sqlResult = cursor.fetchall()

        # print("Print each row and it's columns values")
        for row in sqlResult:
            data_Source_CompetitorRelated = Data_Source_CompetitorRelated()
            data_Source_CompetitorRelated.id = row[0]
            data_Source_CompetitorRelated.competitorId = row[1]
            data_Source_CompetitorRelated.url = row[2]
            data_Source_CompetitorRelated.scraperId = row[3]
            dataSourcesCompetitorRelatedForScraper.append(data_Source_CompetitorRelated)

        return dataSourcesCompetitorRelatedForScraper



    except (Exception, psycopg2.Error) as error:

        print("Error while connecting to PostgreSQL", error)

        # TODO: define specific exception

        raise Exception("Could not pull dataSourcesProductRelatedForScraper from DB.")


    finally:

        if connection:
            cursor.close()

            connection.close()

            # print("PostgreSQL connection is closed")

def getWordsForNewsletterWords(competitor_id):
    connection = None
    dataSourcesCompetitorRelatedForScraper = []

    try:
        words = ""
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime

        cursor.execute("SELECT title FROM ft_newsletter WHERE ft_newsletter.competitor_id ='" + str(competitor_id) + "'")
        sqlResult = cursor.fetchall()

        # print("Print each row and it's columns values")
        for row in sqlResult:
            words = words + " " + row[0]

        return words

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not pull dataSourcesProductRelatedForScraper from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")
