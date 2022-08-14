class Fact_SimilarWeb_Zielgruppendemografie():

    def __init__(self):
        self.id = None
        #Instead of competitor, it would make sense to add the dataSource_competitorRelatedId here so that the source of information is linked
        self.competitorId = None
        self.timestamp = None
        self.fact_timestamp = None
        self.female = None
        self.male = None
        # 18-24
        self.firstAge = None
        # 25-34
        self.secondAge = None
        # 35-44
        self.thirdAge = None
        # 45-54
        self.fourthAge = None
        # 55-64
        self.fifthAge = None
        # 65+
        self.sixthAge = None

    def __str__(self):
        return "ID: " + self.id + "; CompetitorId:" + self.competitorId + "; Timestamp: " + self.timestamp + "; FactTimestamp: " + self.fact_timestamp + "; Female: " + self.female + "; Male: " + self.male + "; FirstAge: " + self.firstAge + "; SecondAge: " + self.secondAge + "; ThirdAge: " + self.thirdAge + "; FourthAge: " + self.fourthAge + "; FifthAge: " + self.fifthAge + "; SixthAge: " + self.sixthAge