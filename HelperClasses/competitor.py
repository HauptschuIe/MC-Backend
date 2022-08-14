class Competitor():

    def __init__(self):
        self.id = None
        self.description = None
        self.abbreviation = None

    def __str__(self):
        return "ID: " + self.id + "; Description: " + self.description + "; Abbreviation: " + self.abbreviation