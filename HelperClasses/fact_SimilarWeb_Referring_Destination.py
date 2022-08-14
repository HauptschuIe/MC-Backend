class Fact_SimilarWeb_Referring_Destination():

    def __init__(self):
        self.id = None
        self.competitorId = None
        self.timestamp = None
        self.referringDestinationSite = None
        self.referringDestination = None
        self.share = None

    def __str__(self):
        return "ID: " + self.id + "; CompetitorId: " + self.competitorId + "; Timestamp: " + self.timestamp + "; ReferringDestinationSite: " + self.referringDestinationSite + "; ReferringDestination: " + self.referringDestination + "; Share: " + self.share