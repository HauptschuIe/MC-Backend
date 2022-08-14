import datetime
import psycopg2
import requests
from HelperClasses.competitor import Competitor
from Middleware.config import config
from HelperClasses.fact_SimilarWeb_Visitor import *
from HelperClasses.fact_SimilarWeb_Marketing_Channels import *
from HelperClasses.fact_SimilarWeb_Keywords import *
from HelperClasses.fact_SimilarWeb_Zielgruppendemografie import *

#DB query to insert list of fact_SimilarWeb_Visitor objects
def insertFacts_SimilarWeb_Visitor(facts_SimilarWeb_Visitor):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_SimilarWeb_Visitor in facts_SimilarWeb_Visitor:
            if type(fact_SimilarWeb_Visitor) is Fact_SimilarWeb_Visitor:
                cursor.execute(
                    #Insert totalVisitors, avgVisitDuration, pagesPerVisit, jumpOffRate into DB (will only work if they are not none anymore)
                    "INSERT INTO public.ft_visitors (competitor_id, timestamp, total_visitors, avg_visit_duration, pages_per_visit, jump_off_rate, fact_timestamp) VALUES ("
                        + str(fact_SimilarWeb_Visitor.competitorId) + ", '" + str(fact_SimilarWeb_Visitor.timestamp) + "' , "
                        + str(fact_SimilarWeb_Visitor.totalVisitors) + ", " + str(fact_SimilarWeb_Visitor.avgVisitDuration) + ", "
                        + str(fact_SimilarWeb_Visitor.pagesPerVisit) + ", " + str(fact_SimilarWeb_Visitor.jumpOffRate) + ", '" + str(fact_SimilarWeb_Visitor.fact_timestamp) + "');")
            else:
                # TODO: define specific exception
                raise ValueError("Could not insert Fact. Type of fact is not Fact_SimilarWeb_Visistor.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_SimilarWeb_Visitor into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")

#DB query to insert list of fact_SimilarWeb_Marketing_Channels objects
def insertFacts_SimilarWeb_Marketing_Channels(facts_SimilarWeb_Marketing_Channels):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_SimilarWeb_Marketing_Channels in facts_SimilarWeb_Marketing_Channels:
            if type(fact_SimilarWeb_Marketing_Channels) is Fact_SimilarWeb_Marketing_Channels:
                cursor.execute(
                    "INSERT INTO public.ft_marketing_channels (competitor_id, timestamp, marketing_channel, share, fact_timestamp) VALUES ("
                        + str(fact_SimilarWeb_Marketing_Channels.competitorId) + ", '" + str(fact_SimilarWeb_Marketing_Channels.timestamp) + "' , '"
                        + str(fact_SimilarWeb_Marketing_Channels.marketing_channel) + "', " + str(fact_SimilarWeb_Marketing_Channels.share) + ", '"
                        + str(fact_SimilarWeb_Marketing_Channels.fact_timestamp) + "');")
            else:
                # TODO: define specific exception
                raise ValueError("Could not insert Fact. Type of fact is not Fact_SimilarWeb_Marketing_Channels.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_SimilarWeb_Marketing_Channels into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")

#DB query to insert list of fact_SimilarWeb_Keywords objects
def insertFacts_SimilarWeb_Keywords(facts_SimilarWeb_Keywords):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_SimilarWeb_Keywords in facts_SimilarWeb_Keywords:
            if type(fact_SimilarWeb_Keywords) is Fact_SimilarWeb_Keywords:
                cursor.execute(
                    "INSERT INTO public.ft_traffic_keywords (competitor_id, timestamp, keyword, share, fact_timestamp) VALUES ("
                        + str(fact_SimilarWeb_Keywords.competitorId) + ", '" + str(fact_SimilarWeb_Keywords.timestamp) + "' , '"
                        + str(fact_SimilarWeb_Keywords.keyword) + "', " + str(fact_SimilarWeb_Keywords.share) + ", '"
                        + str(fact_SimilarWeb_Keywords.fact_timestamp) + "');")
            else:
                # TODO: define specific exception
                raise ValueError("Could not insert Fact. Type of fact is not Fact_SimilarWeb_Keywords.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_SimilarWeb_Keywords into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")

#DB query to insert list of fact_SimilarWeb_Zielgruppendemografie objects
def insertFacts_SimilarWeb_Zielgruppendemografie(facts_SimilarWeb_Zielgruppendemografie):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_SimilarWeb_Zielgruppendemografie in facts_SimilarWeb_Zielgruppendemografie:
            if type(fact_SimilarWeb_Zielgruppendemografie) is Fact_SimilarWeb_Zielgruppendemografie:
                cursor.execute(
                    "INSERT INTO public.ft_zielgruppendemografie (competitor_id, timestamp, fact_timestamp, female, male, firstAge, secondAge, thirdAge, fourthAge, fifthAge, sixthAge) VALUES ("
                        + str(fact_SimilarWeb_Zielgruppendemografie.competitorId) + ", '" + str(fact_SimilarWeb_Zielgruppendemografie.timestamp) + "' , '"
                        + str(fact_SimilarWeb_Zielgruppendemografie.fact_timestamp) + "', " + str(fact_SimilarWeb_Zielgruppendemografie.female) + ", " + str(fact_SimilarWeb_Zielgruppendemografie.male) + ", " + str(fact_SimilarWeb_Zielgruppendemografie.firstAge) + ", " + str(fact_SimilarWeb_Zielgruppendemografie.secondAge) + ", " + str(fact_SimilarWeb_Zielgruppendemografie.thirdAge) + ", " + str(fact_SimilarWeb_Zielgruppendemografie.fourthAge) + ", " + str(fact_SimilarWeb_Zielgruppendemografie.fifthAge) + ", " + str(fact_SimilarWeb_Zielgruppendemografie.sixthAge) + ");")
            else:
                # TODO: define specific exception
                raise ValueError("Could not insert Fact. Type of fact is not Fact_SimilarWeb_Zielgruppendemografie.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_SimilarWeb_Zielgruppendemografie into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Zielgruppendemografie Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")

#DB query to insert list of fact_SimilarWeb_Referring_Destination objects
def insertFacts_SimilarWeb_Referring_Destination(facts_SimilarWeb_Referring_Destination):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_SimilarWeb_Referring_Destination in facts_SimilarWeb_Referring_Destination:
            cursor.execute(
                #Insert referring_destination_site, referring_destination, share into DB (will only work if they are not none anymore)
                "INSERT INTO public.ft_referring_destination (competitor_id, timestamp, referring_destination_site, referring_destination, share) VALUES ("
                    + str(fact_SimilarWeb_Referring_Destination.competitorId) + ", '" + str(fact_SimilarWeb_Referring_Destination.timestamp) + "' , '"
                    + str(fact_SimilarWeb_Referring_Destination.referringDestinationSite) + "', '" + str(fact_SimilarWeb_Referring_Destination.referringDestination) + "', '"
                    + str(fact_SimilarWeb_Referring_Destination.share) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_SimilarWeb_Referring_Destination into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")

#DB query to insert list of fact_ShoppingPopularity objects
def insertFacts_ShoppingPopularity(facts_ShoppingPopularity):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_ShoppingPopularity in facts_ShoppingPopularity:
            cursor.execute(
                "INSERT INTO public.ft_shopping_popularity (competitor_id, product_id, request_timestamp, fact_timestamp, latest, popularity_score) VALUES ("
                    + str(fact_ShoppingPopularity.competitorId) + ", " + str(fact_ShoppingPopularity.productId) + ", '" + str(fact_ShoppingPopularity.requestTimestamp) + "', '"
                    + str(fact_ShoppingPopularity.factTimestamp) + "', " + str(fact_ShoppingPopularity.latest)+ ", '" + str(fact_ShoppingPopularity.popularityScore) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_SimilarWeb_Referring_Destination into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            print("Data successful inserted into PostgreSQL")
            connection.close()
            print("PostgreSQL connection is closed")

def insertFacts_ProductInformations(facts_ProductInformations):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_ProductInformations in facts_ProductInformations:
            cursor.execute(
                "INSERT INTO public.ft_product_informations (competitor_id, product_id, timestamp, price, price_status_id, availability_status_id) VALUES ("
                + str(fact_ProductInformations.competitorId) + "," + str(fact_ProductInformations.productId) + ",'" + str(
                    fact_ProductInformations.timestamp) + "' , "
                + str(fact_ProductInformations.price) + ", " + str(fact_ProductInformations.price_status_id) + ", " + str(
                    fact_ProductInformations.availability_status_id) + ");")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_ProductInformations into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()
            
def insertFacts_LocationsInformations(facts_LocationInformations):
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for fact_LocationInformation in facts_LocationInformations:
            cursor.execute(
                "INSERT INTO public.ft_locations (competitor_id, city, postal_code, street, latitude, longitude, timestamp, name) VALUES ("
                + str(fact_LocationInformation.competitorId) + ",'" + str(fact_LocationInformation.city) + "'," + str(
                    fact_LocationInformation.postal_code) + " , '"
                + str(fact_LocationInformation.street) + "', " + str(fact_LocationInformation.latitude) + ", " + str(
                    fact_LocationInformation.longitude) + " , '" + str(fact_LocationInformation.timestamp) + "', '" + str(fact_LocationInformation.name) + "');")

        cursor.execute("TRUNCATE TABLE public.ft_locations_numbers")

        cursor.execute("SELECT description AS Competitor, count(subselect) AS Number FROM"
        + "(SELECT longitude, competitor_id, description"
        + "FROM ft_locations, dt_competitors"
        + "WHERE ft_locations.competitor_id = dt_competitors.id AND"
        + "competitor_id IN (3,4,5,6)"
        + "GROUP BY longitude, competitor_id, description) AS subselect"
        + "GROUP BY competitor_id, description"
        + "ORDER BY competitor_id asc")

        sqlResult = cursor.fetchall()

        for row in sqlResult:
            cursor.execute(
                "INSERT INTO public.ft_locations_numbers (competitor_id, numbers, timestamp) VALUES ("
                +str(row[0]) + "," + str(row[1]) + " , '" + str(datetime.now()) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_ProductInformations into DB.")

    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()

def insertFacts_CompetitorValuation(facts_CompetitorValuation):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_competitor_valuation in facts_CompetitorValuation:
            cursor.execute("INSERT INTO public.ft_competitor_valuation(competitor_id, total, culture_values, diversity_inclusion, work_life_balance, management_level, "\
                                "benefits, opportunities, recommendation, commitment_gf, pos_prognose, timestamp) VALUES ("
                                + str(fact_competitor_valuation.competitor_id) + ", " + str(fact_competitor_valuation.total) + ", " + str(fact_competitor_valuation.culture_values) + ", "
                                + str(fact_competitor_valuation.diversity_inclusion) + ", " + str(fact_competitor_valuation.work_life_balance) + ", " + str(fact_competitor_valuation.management_level) + ", "
                                + str(fact_competitor_valuation.benefits) + ", " + str(fact_competitor_valuation.opportunities) + ", " + str(fact_competitor_valuation.recommendation) + ", "
                                + str(fact_competitor_valuation.commitment_gf) + ", " + str(fact_competitor_valuation.pos_prognose) + ", '" + str(fact_competitor_valuation.timestamp) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_CompetitorValuation into DB.")
    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()
            
def insertFacts_CompetitorInterview(facts_CompetitorInterview):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_interview_interview in facts_CompetitorInterview:
            print(fact_interview_interview.other)
            cursor.execute("INSERT INTO public.dt_interview_experience(positiv, negativ, neutral) VALUES ("
                           + str(fact_interview_interview.positiv) + ", " + str(
                fact_interview_interview.negativ) + ", " + str(fact_interview_interview.neutral) + ");")

            cursor.execute(
                "INSERT INTO public.dt_interview_invitation(online, recruiter, recommendation, university_recruiter, personal, agency, other) VALUES ("
                + str(fact_interview_interview.online) + ", " + str(fact_interview_interview.recruiter) + ", " + str(fact_interview_interview.recommendation) + ", "
                + str(fact_interview_interview.university_recruiter) + ", " + str(fact_interview_interview.personal) + ", " + str(fact_interview_interview.agency) + ", "
                + str(fact_interview_interview.other) + ");")

            cursor.execute(
                "INSERT INTO public.ft_interview_valuation(competitor_id, difficulty, timestamp) VALUES (" + str(
                    fact_interview_interview.competitor_id) + ","
                + str(fact_interview_interview.difficulty) + ",'"
                + str(fact_interview_interview.timestamp) + "');")


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_CompetitorInterview into DB.")
    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()
            
def insertFacts_CustomerReview(facts_CustomerReview):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_customer_review in facts_CustomerReview:
            cursor.execute("INSERT INTO public.ft_customer_review(competitor_id, total, total_description, excellent, good, acceptable, deficient, insufficient, timestamp, total_reviews)" \
                                " VALUES (" + str(fact_customer_review.competitor_id) + ", " + str(fact_customer_review.total) + ", '" + str(fact_customer_review.total_description) + "', "
                                + str(fact_customer_review.excellent) + ", " + str(fact_customer_review.good) + ", " + str(fact_customer_review.acceptable) + ", "
                                + str(fact_customer_review.deficient) + ", " + str(fact_customer_review.insufficient) + ", '" + str(fact_customer_review.timestamp) + "', " + str(fact_customer_review.total_reviews) +");")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_CustomerReview into DB.")
    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()
            
def insertFacts_CustomerReviewSourceNew(facts_CustomerReviewNew):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE public.ft_new_evaluations")
        for fact_evaluation_per_source_review in facts_CustomerReviewNew:


            cursor.execute("INSERT INTO public.ft_new_evaluations(competitor_id, sources_of_evaluations_id, excellent, good, acceptable, deficient, insufficient, month, year, timestamp)" \
                                " VALUES (" + str(fact_evaluation_per_source_review.competitor_id) + ", " + str(fact_evaluation_per_source_review.sources_of_evaluations_id) + ", '" + str(fact_evaluation_per_source_review.excellent) + "', "
                                + str(fact_evaluation_per_source_review.good) + ", " + str(fact_evaluation_per_source_review.acceptable) + ", " + str(fact_evaluation_per_source_review.deficient) + ", "
                                + str(fact_evaluation_per_source_review.insufficient) + ", '" + str(fact_evaluation_per_source_review.month) + "', '"
                                + str(fact_evaluation_per_source_review.year) + "', '" + str(fact_evaluation_per_source_review.timestamp) + "');")


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_CustomerReviewNew into DB.")
    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()

def insertFacts_Newsletter(facts_Newsletter):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        for fact_newsletter in facts_Newsletter:
            cursor.execute("INSERT INTO public.ft_newsletter(competitor_id, title, date, timestamp, body)" \
                                " VALUES (" + str(fact_newsletter.competitor_id) + ", '" + str(fact_newsletter.title) + "', '" + str(fact_newsletter.date) + "','"
                                 + str(fact_newsletter.timestamp) + "', '" + str(fact_newsletter.body) +"');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_Newsletter into DB.")
    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()
    
def insertFacts_NewsletterWords(facts_NewsletterWords):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE public.ft_newsletterwords")
        for fact_newsletterWord in facts_NewsletterWords:
            cursor.execute("INSERT INTO public.ft_newsletterwords(competitor_id, word, quantity, rank, timestamp)" \
                                " VALUES (" + str(fact_newsletterWord.competitor_id) + ", '" + str(fact_newsletterWord.word) + "', '" + str(fact_newsletterWord.quantity) + "',"
                                 + str(fact_newsletterWord.rank) + ",'" + str(fact_newsletterWord.timestamp) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_NewsletterWords into DB.")
    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()

def insertFacts_NewsletterWordcloud(facts_NewsletterWordcloud):
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE public.ft_newsletterwordcloud")
        for fact_newsletterWordcloud in facts_NewsletterWordcloud:
            cursor.execute("INSERT INTO public.ft_newsletterwordcloud(competitor_id, term, timestamp)" \
                                " VALUES (" + str(fact_newsletterWordcloud.competitor_id) + ", '" + str(fact_newsletterWordcloud.term) + "', '" 
                                 + str(fact_newsletterWordcloud.timestamp) + "');")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # TODO: define specific exception
        raise Exception("Could not insert Fact_NewsletterWordcloud into DB.")
    finally:
        if connection:
            cursor.close()
            connection.commit()
            connection.close()