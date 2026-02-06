from backend.Categories.categories import Categories
Groceries = []
Restaurants = []
Entertainment = []
Utilities = []
Transportation = []
Academics = []
Personal_Care = []
Clothing = []
Retail = []
Other = []


class Transaction:
    def __init__(self, merchant, cost, category):
        self.merchant = merchant
        self.cost = cost
        self.category = category

#def categorize_merchants(merchant_name, merchant_cost_list):
#use llm to identify merchant

