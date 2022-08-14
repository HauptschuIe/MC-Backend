import numpy as np
import psycopg2
from Testing.test_config import config

n = 12
latest_prices = np.zeros(shape=[6, 14])


def getTable():
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Read PostgreSQL purchase timestamp value into Python datetime
        cursor.execute("SELECT * FROM public.ft_product_informations;")
        sqlResult = cursor.fetchall()

        return sqlResult

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL. ", error)
        # TODO: define specific exception
        raise Exception("Could not pull proxies from DB.")

    finally:
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")


def replaceNull(id, value):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("UPDATE public.ft_product_informations SET price = '" +
                       str(value) + "' WHERE id = '" + str(id) + "';")

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


table = getTable()

# get first price of each product - competitor combination
for x in table:
    if (latest_prices[x[0] - 1][x[1] - 1]) == 0 or np.isnan(
            latest_prices[x[0] - 1][x[1] - 1]) == True:
        latest_prices[x[0] - 1][x[1] - 1] = x[3]
    if (not 0 in latest_prices) and (np.isnan(np.min(latest_prices)) == False):
        print("ufff")
        break

# replace Null Values
for y in table:
    if (y[3] == None) and (np.isnan(latest_prices[y[0] - 1][y[1] - 1])
                           == False):
        replaceNull(y[6], latest_prices[y[0] - 1][y[1] - 1])
    else:
        latest_prices[y[0] - 1][y[1] - 1] = y[3]
