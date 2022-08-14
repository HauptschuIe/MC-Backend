class Product():

    def __init__(self):
        self.id = None
        self.description = None
        self.categoryId = None
        self.active = None

    def __str__(self):
        return "ID: " + self.id + "; Description: " + self.description + "; CategoryId: " + self.categoryId + "; Active: " + self.active