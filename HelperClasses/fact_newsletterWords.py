class Fact_NewsletterWords():

    def __init__(self):
        self.id = None
        self.competitor_id = None
        self.word = None
        self.quantity = None
        self.rank = None
        self.timestamp = None


    def __str__(self):
        return "id: " + self.id + "; competitor_id:" + self.competitor_id + "; word: " + self.word +\
               "; quantity: " + self.quantity + "; rank: " + self.rank + "; timestamp: " + self.timestamp
