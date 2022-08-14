class Fact_CustomerReview():

    def __init__(self):
        self.id = None
        self.competitor_id = None
        self.total = None
        self.total_description = None
        self.excellent = None
        self.good = None
        self.acceptable = None
        self.deficient = None
        self.insufficient = None
        self.timestamp = None
        self.total_reviews = None

    def __str__(self):
        return "id: " + self.id + "; competitor_id:" + self.competitor_id + "; total: " + self.total + \
               "; total_description: " + self.total_description + "; excellent: " + self.excellent + \
               "; good: " + self.good + "; acceptable: " + self.acceptable + \
               "; deficient: " + self.deficient + "; insufficient: " + self.insufficient + "; timestamp: " + self.timestamp + \
               "; total_reviews: " + self.total_reviews