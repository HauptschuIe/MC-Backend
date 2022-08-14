from itertools import count
from sqlite3 import connect
import psycopg2
from Middleware.config import config


def writeResultsIntoDB(similarWebScraperObject):
    # TODO: SQL Magic
    return None


def writePriceResultsIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Insert Data to PostgreSQL into ft_product_informations
        cursor.execute(
            "INSERT INTO public.ft_product_informations (competitor_id, product_id, timestamp, price, price_status_id, availability_status_id) VALUES ("
            + str(ScraperObject.anbieterid) + "," +
            str(ScraperObject.produktid) + ",'" + str(ScraperObject.date) +
            "' , " + str(ScraperObject.product_price) + ", " +
            str(ScraperObject.price_status) + ", " +
            str(ScraperObject.availability) + ");")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")


def writeLocationsResultsIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Insert Data to PostgreSQL into ft_locations
        cursor.execute(
            "INSERT INTO public.ft_locations (competitor_id, city, postal_code, street, latitude, longitude, timestamp, name) VALUES "
            + ScraperObject.insertString + ";")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")


def writeCompetitorValuationResultsIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_competitor_valuation in ScraperObject:
            cursor.execute("INSERT INTO public.ft_competitor_valuation(competitor_id, total, culture_values, diversity_inclusion, work_life_balance, management_level, "\
                                "benefits, opportunities, recommendation, commitment_gf, pos_prognose, timestamp) VALUES ("
                                + str(fact_competitor_valuation.competitor_id) + ", " + str(fact_competitor_valuation.total) + ", " + str(fact_competitor_valuation.culture_values) + ", "
                                + str(fact_competitor_valuation.diversity_inclusion) + ", " + str(fact_competitor_valuation.work_life_balance) + ", " + str(fact_competitor_valuation.management_level) + ", "
                                + str(fact_competitor_valuation.benefits) + ", " + str(fact_competitor_valuation.opportunities) + ", " + str(fact_competitor_valuation.recommendation) + ", "
                                + str(fact_competitor_valuation.commitment_gf) + ", " + str(fact_competitor_valuation.pos_prognose) + ", '" + str(fact_competitor_valuation.timestamp) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")


def writeInterviewValuationResultsIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        # Insert Data to PostgreSQL into ft_competitor_valuation
        for fact_interview_valuation in ScraperObject:
            cursor.execute(
                "INSERT INTO public.dt_interview_experience(positiv, negativ, neutral) VALUES ("
                + str(fact_interview_valuation.positiv) + ", " +
                str(fact_interview_valuation.negativ) + ", " +
                str(fact_interview_valuation.neutral) + ");")

            cursor.execute(
                "INSERT INTO public.dt_interview_invitation(online, recruiter, recommendation, university_recruiter, personal, agency, other) VALUES ("
                + str(fact_interview_valuation.online) + ", " +
                str(fact_interview_valuation.recruiter) + ", " +
                str(fact_interview_valuation.recommendation) + ", " +
                str(fact_interview_valuation.university_recruiter) + ", " +
                str(fact_interview_valuation.personal) + ", " +
                str(fact_interview_valuation.agency) + ", " +
                str(fact_interview_valuation.other) + ");")

            cursor.execute(
                "INSERT INTO public.ft_interview_valuation(competitor_id, difficulty, timestamp) VALUES ("
                + str(fact_interview_valuation.competitor_id) + "," +
                str(fact_interview_valuation.difficulty) + ",'" +
                str(fact_interview_valuation.timestamp) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")


def writeCustomerReviewResultsIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_customer_review in ScraperObject:
            cursor.execute("INSERT INTO public.ft_customer_review(competitor_id, total, total_description, excellent, good, acceptable, deficient, insufficient, timestamp, total_reviews)" \
                                " VALUES (" + str(fact_customer_review.competitor_id) + ", " + str(fact_customer_review.total) + ", '" + str(fact_customer_review.total_description) + "', "
                                + str(fact_customer_review.excellent) + ", " + str(fact_customer_review.good) + ", " + str(fact_customer_review.acceptable) + ", "
                                + str(fact_customer_review.deficient) + ", " + str(fact_customer_review.insufficient) + ", '" + str(fact_customer_review.timestamp) + "', " + str(fact_customer_review.total_reviews) +");")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")


def writeEvaluationPerSourceResultsIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_evaluation_per_source_review in ScraperObject:
            cursor.execute("INSERT INTO public.ft_evaluation_per_source(competitor_id, sources_of_evaluations_id, excellent, good, acceptable, deficient, insufficient, timestamp)" \
                                " VALUES (" + str(fact_evaluation_per_source_review.competitor_id) + ", " + str(fact_evaluation_per_source_review.sources_of_evaluations_id) + ", '" + str(fact_evaluation_per_source_review.excellent) + "', "
                                + str(fact_evaluation_per_source_review.good) + ", " + str(fact_evaluation_per_source_review.acceptable) + ", " + str(fact_evaluation_per_source_review.deficient) + ", "
                                + str(fact_evaluation_per_source_review.insufficient) + ", '" + str(fact_evaluation_per_source_review.timestamp) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")


def writeNewEvaluationsIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_evaluation_per_source_review in ScraperObject:
            cursor.execute("INSERT INTO public.ft_new_evaluations(competitor_id, sources_of_evaluations_id, excellent, good, acceptable, deficient, insufficient, month, year, timestamp)" \
                                " VALUES (" + str(fact_evaluation_per_source_review.competitor_id) + ", " + str(fact_evaluation_per_source_review.sources_of_evaluations_id) + ", '" + str(fact_evaluation_per_source_review.excellent) + "', "
                                + str(fact_evaluation_per_source_review.good) + ", " + str(fact_evaluation_per_source_review.acceptable) + ", " + str(fact_evaluation_per_source_review.deficient) + ", "
                                + str(fact_evaluation_per_source_review.insufficient) + ", '" + str(fact_evaluation_per_source_review.month) + "', '"
                                + str(fact_evaluation_per_source_review.year) + "', '" + str(fact_evaluation_per_source_review.timestamp) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")


#DB query to insert youtube_channel_data into the database
def writeYoutubeChannelDataIntoDB(ScraperObject):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()

        insert_query = """ INSERT INTO public.ft_youtube_channel_data(competitor_id, view_count, subscriber_count, video_count, timestamp) VALUES (%s, %s, %s, %s, %s) """
        record = (ScraperObject[0], ScraperObject[1], ScraperObject[2],
                  ScraperObject[3], ScraperObject[4])

        cursor.execute(insert_query, record)
        connection.commit()

        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL! \n", error)
        raise Exception("Error while connecting to PostgreSQL!")
    finally:
        if connection:
            cursor.close()
            connection.close()


#DB query to insert twitter_account_data into the database
def writeTwitterAccountDataIntoDB(ScraperObject):
    connect = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        insert_query = """ INSERT INTO public.ft_twitter_account_data(competitor_id, followers_count, following_count, tweet_count, timestamp) VALUES (%s, %s, %s, %s, %s) """
        record = (ScraperObject[0], ScraperObject[1], ScraperObject[2], ScraperObject[3], ScraperObject[4])

        cursor.execute(insert_query, record)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL! \n", error)
        raise Exception("Error while connecting to PostgreSQL!")
    finally:
        if connection:
            cursor.close()
            connection.close()


# DB query to insert twitter_comments_data into the database
def writeTwitterCommentsDataIntoDB(ScraperObject):
    connect = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        insert_query = """ INSERT INTO public.ft_twitter_comments_data(competitor_id, timestamp, tweet_text, sentiment, confidence) VALUES (%s, %s, %s, %s, %s) """
        record = (ScraperObject[0], ScraperObject[1], ScraperObject[2],
                  ScraperObject[3], ScraperObject[4])

        cursor.execute(insert_query, record)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL! \n", error)
        raise Exception("Error while connecting to PostgreSQL!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            
# DB query to insert newsletter_data into the database
def writeNewsletterDataIntoDB(ScraperObject):
    connect = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        insert_query = """ INSERT INTO public.ft_newsletter(competitor_id, title, date, timestamp, body) VALUES (%s, %s, %s, %s, %s) """
        record = (ScraperObject[0], ScraperObject[1], ScraperObject[2],
                  ScraperObject[3], ScraperObject[4])

        cursor.execute(insert_query, record)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL! \n", error)
        raise Exception("Error while connecting to PostgreSQL!")
    finally:
        if connection:
            cursor.close()
            connection.close()


#DB query to insert twitter_tweets_data into the database
def writeTwitterTweetsDataIntoDB(ScraperObject):
    connect = None
    try: 
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        insert_query = """ INSERT INTO public.ft_twitter_tweets_data(competitor_id, tweet_text, timestamp, tweet_retweet_count, tweet_reply_count, tweet_like_count, tweet_quote_count) VALUES (%s, %s, %s, %s, %s, %s, %s) """
        record = (ScraperObject[0], ScraperObject[1], ScraperObject[2], ScraperObject[3], ScraperObject[4], ScraperObject[5], ScraperObject[6])

        cursor.execute(insert_query, record)
        connection.commit()

        count = cursor.rowcount
        print(count, "Record inserted successfully into table")
    
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL! \n", error)
        raise Exception("Error while connecting to PostgreSQL!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
