import datetime
import psycopg2
import requests
from Middleware.config import config


def url_rueckgabe():
    connection = None
    urls = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute("SELECT similarweb_id from dim_competitors")
        dim_competitors = cursor.fetchall()

        print("Print each row and it's columns values")
        for row in dim_competitors:
            urls.append(row[0])
        print(urls)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return urls


def url_rueckgabe_product_sources_fetchall(competitor_id, scraper_id):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime

        cursor.execute("SELECT ps.product_id, ps.url FROM dt_product_sources ps, dt_products p WHERE ps.scraper_id = " + str(scraper_id) + " AND ps.product_id = "
                       "p.id AND ps.competitor_id = " + str(competitor_id) + " AND p.active = true ORDER BY ps.product_id")
        rows = cursor.fetchall()


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return rows


def url_rueckgabe_competitor_sources_fetchone(competitor_id, scraper_id):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime

        cursor.execute("SELECT cs.url FROM dt_competitor_sources cs WHERE cs.scraper_id = " + str(scraper_id) + " AND cs.competitor_id = " + str(competitor_id))
        rows = cursor.fetchone()
        print(rows)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return rows


def url_rueckgabe_competitor_sources_fetchall(scraper_id):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime

        cursor.execute("SELECT cs.url, cs.competitor_id FROM dt_competitor_sources cs WHERE cs.scraper_id = " + str(scraper_id))
        rows = cursor.fetchall()


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return rows
