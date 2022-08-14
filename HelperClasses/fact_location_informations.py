class Fact_LocationInformations():

    def __init__(self):
        self.id = None
        self.competitorId = None
        self.timestamp = None
        self.postal_code = None
        self.city = None
        self.street = None
        self.latitude = None
        self.longitude = None
        self.name = None

    def __str__(self):
        return "id: " + self.id + "; competitorId:" + self.competitorId + "; postal_code: " + self.postal_code + "; timestamp: " + self.timestamp + "; city: " + self.city + "; street: " + self.street + "; latitude: " + self.latitude + "; longitude: " + self.longitude + "; name: " + self.name