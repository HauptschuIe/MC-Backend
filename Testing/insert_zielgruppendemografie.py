from datetime import datetime
import psycopg2
from Testing.test_config import config

time = datetime.now()
data_competitor = []

data_competitor.insert(0, 1)
data_competitor.insert(1, time)
data_competitor.insert(2, '2022-04-01 00:00:00')
data_competitor.insert(3, 32.37)
data_competitor.insert(4, 67.63)
data_competitor.insert(5, 21.97)
data_competitor.insert(6, 27.86)
data_competitor.insert(7, 19.22)
data_competitor.insert(8, 14.86)
data_competitor.insert(9, 8.92)
data_competitor.insert(10, 7.16)
print(data_competitor)


#DB query to insert list of fact_SimilarWeb_Zielgruppendemografie objects
def insertFacts_SimilarWeb_Zielgruppendemografie():
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        insert_query = """ INSERT INTO public.ft_zielgruppendemografie(competitor_id, timestamp, fact_timestamp, female, male, first_age, second_age, third_age, fourth_age, fifth_age, sixth_age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        record = (data_competitor[0], data_competitor[1], data_competitor[2],
                  data_competitor[3], data_competitor[4], data_competitor[5],
                  data_competitor[6], data_competitor[7], data_competitor[8],
                  data_competitor[9], data_competitor[10])

        cursor.execute(insert_query, record)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception(
            "Could not insert Fact_SimilarWeb_Zielgruppendemografie into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print(
                "Zielgruppendemografie Data successful inserted into PostgreSQL"
            )
            connection.close()
            print("PostgreSQL connection is closed")


insertFacts_SimilarWeb_Zielgruppendemografie()