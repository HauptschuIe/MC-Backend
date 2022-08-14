class Fact_ProductInformations():

    def __init__(self):
        self.id = None
        self.productId = None
        self.competitorId = None
        self.timestamp = None
        self.price = None
        self.price_status_id = None
        self.availability_status_id = None


    def __str__(self):
        return "id: " + self.id + "; product_id:" + self.productId + "; competitorId: " + self.competitorId + "; timestamp: " + self.timestamp + "; price: " + self.price + "; price_status_id: " + self.price_status_id + "; availability_status_id: " + self.availability_status_id