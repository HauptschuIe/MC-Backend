class Fact_Newsletter():

    def __init__(self):
        self.id = None
        self.competitor_id = None
        self.title = None
        self.date = None
        self.timestamp = None
        self.body = None


    def __str__(self):
        return "id: " + self.id + "; competitor_id:" + self.competitor_id + "; title: " + self.title +\
               "; date: " + self.date + "; timestamp: " + self.timestamp + "; body: " + self.body
