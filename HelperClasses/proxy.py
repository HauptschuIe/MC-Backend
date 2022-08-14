class ScraperProxy():

    def __init__(self):
        self.id = None
        self.address = None
        self.scraperId = None
        self.dateLastUsed = None
        self.active = None

    def __str__(self):
        return "ID: " + self.id