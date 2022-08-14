class Fact_ShoppingPopularity():

    def __init__(self):
        self.id = None
        self.competitorId = None
        self.requestTimestamp = None
        #GoogleTrends provides a list of results with a score for each date -> the date related to the fact is not the date the fact was created / requested
        self.factTimestamp = None
        self.latest = None
        self.productId = None
        self.popularityScore = None

    def __str__(self):
        return "ID: " + self.id + "; CompetitorId:" + self.competitorId + "; RequestTimestamp: " + self.requestTimestamp + "; FactTimestamp: " + self.factTimestamp + "; Latest: " + self.latest + "; ProductId: " + self.productId + "; PopularityScore: " + self.popularityScore