class Fact_CustomerReviewNew():

    def __init__(self):
        self.id = None
        self.competitor_id = None
        self.sources_of_evaluations_id = None
        self.excellent = None
        self.good = None
        self.acceptable = None
        self.deficient = None
        self.insufficient = None
        self.month = None
        self.year = None
        self.timestamp = None


    def __str__(self):
        return "id: " + self.id + "; competitor_id:" + self.competitor_id + "; sources_of_evaluations_id: " + self.sources_of_evaluations_id +\
               "; excellent: " + self.excellent + "; good: " + self.good +\
               "; acceptable: " + self.acceptable + "; deficient: " + self.deficient +\
               "; insufficient: " + self.insufficient + "; month: " + self.month + "; year: " + self.year +\
               "; timestamp: " + self.timestamp