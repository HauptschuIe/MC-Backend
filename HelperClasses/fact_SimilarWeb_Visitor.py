class Fact_SimilarWeb_Visitor():

    def __init__(self):
        self.id = None
        #Instead of competitor, it would make sense to add the dataSource_competitorRelatedId here so that the source of information is linked
        self.competitorId = None
        self.timestamp = None
        self.totalVisitors = None
        self.avgVisitDuration = None
        self.pagesPerVisit = None
        self.jumpOffRate = None
        self.fact_timestamp = None

    def __str__(self):
        return "ID: " + self.id + "; CompetitorId:" + self.competitorId + "; Timestamp: " + self.timestamp + "; TotalVisitors: " + self.totalVisitors + "; AvgVisitDuration: " + self.avgVisitDuration + "; PagesPerVisit: " + self.pagesPerVisit + "; JumpOffRate: " + self.jumpOffRate