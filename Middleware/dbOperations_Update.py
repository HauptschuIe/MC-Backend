import datetime
import psycopg2
import requests
from HelperClasses.competitor import Competitor
from Middleware.config import config

#DB query to insert list of fact_SimilarWeb_Visitor objects
def updateFacts_ShoppingPopularity_LatestToFalse():
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE ft_shopping_popularity SET latest = FALSE;")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not set all latest flags of Facts for ShoppingPopularity to false.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successfully updates into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")

def updateProxyDateLastUsed(sprox):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE dt_proxies SET date_last_used = '" + datetime.datetime.strftime(sprox.dateLastUsed,'%Y-%m-%d') + "' WHERE id = '" + str(sprox.id) + "';")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not update dateLastUsed of proxy.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successfully updates into PostgreSQL")
            connection.close()
            #print("PostgreSQL connection is closed")