class Fact_NewsletterWordcloud():

    def __init__(self):
        self.id = None
        self.competitor_id = None
        self.term = None
        self.timestamp = None


    def __str__(self):
        return "id: " + self.id + "; competitor_id:" + self.competitor_id + "; term: " + self.term +\
               "; timestamp: " + self.timestamp
