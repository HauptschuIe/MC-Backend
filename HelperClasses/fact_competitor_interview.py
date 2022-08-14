class Fact_CompetitorInterview():

    def __init__(self):
        self.id = "Null"
        self.competitor_id = "Null"
        self.positiv = "Null"
        self.negativ = "Null"
        self.neutral = "Null"
        self.online = "Null"
        self.recruiter = "Null"
        self.recommendation = "Null"
        self.university_recruiter = "Null"
        self.personal = "Null"
        self.agency = "Null"
        self.other = "Null"
        self.difficulty = "Null"
        self.timestamp = "Null"

    def __str__(self):
        return "id: " + self.id + "; competitorId:" + self.competitorId + "; positiv: " + self.positiv +\
               "; negativ: " + self.negativ + "; neutral: " + self.neutral +\
               "; online: " + self.online + "; recruiter: " + self.recruiter +\
               "; recommendation: " + self.recommendation + "; university_recruiter: " + self.university_recruiter + "; personal: " + self.personal +\
               "; agency: " + self.agency + "; other: " + self.other + \
               "; difficulty: " + self.difficulty + "; timestamp: " + self.timestamp