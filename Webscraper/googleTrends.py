import datetime
from HelperClasses.fact_ShoppingPopularity import Fact_ShoppingPopularity
from HelperClasses.scraper import Scraper
from Middleware.read import url_rueckgabe
from Middleware.create import writeResultsIntoDB
from DataTransformation.transformation import *
from Middleware.dbOperations_Read import *
from Middleware.dbOperations_Insert import *
from Middleware.dbOperations_Update import *
import pytrends                        
from pytrends.request import TrendReq

#Language German, timezone CET, scope last 12 months (will return weekly basis), Geo Germany
trendsHl = 'de-DE'
trendsTz = -60
trendsScope = 'today 12-m'
trendsGeo = 'DE'

class Scraper_GoogleTrends(Scraper):

    #ScrapeKPIs; return a list of Fact_SimilarWeb_Visitor objects
    def scrape(self):
        facts = []
        searchStrings = []

        #build one search string out of all dataSource.url
        for dataSource in self.dataSources:
            #assumption: search urls are unique!
            searchStrings.append(dataSource.url)

        #perform call and retrieve results 
        pytrend = TrendReq(hl=trendsHl, tz=trendsTz)
        pytrend.build_payload(kw_list=searchStrings, timeframe=trendsScope, geo=trendsGeo, gprop='')
        df = pytrend.interest_over_time()
        #returns a data dictionary with the dataSource.url as key and another dictionary as value (whose key is each rows date)
        requestResult = df.to_dict()
        requestTime = datetime.datetime.now()

        for dataSource in self.dataSources:
            #use dictionary to get dataSource object for url, col heading is the search string we used
            requestResultForDataSource = requestResult[dataSource.url]

            #each row is a date; each row has one key in dictionary of requestResultForDataSource
            for dateKey in requestResultForDataSource.keys():
                fact_ShoppingPopularity = Fact_ShoppingPopularity()
                fact_ShoppingPopularity.competitorId = dataSource.competitorId
                fact_ShoppingPopularity.productId = dataSource.productId
                fact_ShoppingPopularity.requestTimestamp = requestTime
                fact_ShoppingPopularity.factTimestamp = dateKey
                fact_ShoppingPopularity.latest = True
                fact_ShoppingPopularity.popularityScore = float(requestResultForDataSource[dateKey])
                
                #print(dataSource.url + "; " + fact_ShoppingPopularity.factTimestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)") + ": " + str(fact_ShoppingPopularity.popularityScore))

                facts.append(fact_ShoppingPopularity)

        return facts

