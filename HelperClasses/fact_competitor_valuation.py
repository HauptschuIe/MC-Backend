class Fact_CompetitorValuation():

    def __init__(self):
        self.id = None
        self.competitorId = None
        self.total = None
        self.culture_values = None
        self.diversity_inclusion = None
        self.work_life_balance = None
        self.management_level = None
        self.benefits = None
        self.opportunities = None
        self.recommendation = None
        self.commitment_gf = None
        self.pos_prognose = None
        self.timestamp = None

    def __str__(self):
        return "id: " + self.id + "; competitorId:" + self.competitorId + "; total: " + self.total +\
               "; culture_values: " + self.culture_values + "; diversity_inclusion: " + self.diversity_inclusion +\
               "; work_life_balance: " + self.work_life_balance + "; management_level: " + self.management_level +\
               "; benefits: " + self.benefits + "; opportunities: " + self.opportunities + "; recommendation: " + self.recommendation +\
               "; commitment_gf: " + self.commitment_gf + "; pos_prognose: " + self.pos_prognose + \
               "; timestamp: " + self.timestamp