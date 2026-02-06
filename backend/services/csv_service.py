import csv
import os
import nltk 
import requests
from dotenv import load_dotenv
from backend.Categories.categories import Categories
from backend.Categories.categorize_csv import Transaction

load_dotenv()
yelp_api_key = os.getenv("YELP_API_KEY")





def ensure_wordnet():
    try:
        from nltk.corpus import wordnet as wn
        wn.synsets("store")
      
    except LookupError:
        nltk.download("wordnet")
    return wn
wn= ensure_wordnet()    

def csv_identify_merchants_costs(file_data):
    
    file_as_text = file_data.decode("utf-8").splitlines()
    #dict iterator
    file_dictionary = csv.DictReader(file_as_text)
    header=file_as_text[0]
    header_parts= header.split(",")

    merchant_synset=set(wn.synsets("merchant", pos=wn.NOUN)) #synonyms for the word merchant 
    cost_synset = set(wn.synsets("cost", pos=wn.NOUN))
    create_merchant_cost_dict(merchant_synset, cost_synset,header_parts, file_dictionary)
   
       

def create_merchant_cost_dict(merchant_synset, cost_synset, header_parts, file_dictionary):
    merchant_cost_list = []
    merchant_header=None
    cost_header=None


    for part in header_parts:
        #if (header) has the same meaning as merchant save it
       
        part_synset=set(wn.synsets(part, pos=wn.NOUN))  

        #COMPARE SYNSETS
        if(merchant_synset & part_synset):
           merchant_header=part#merchant header name
        elif(cost_synset & part_synset):
            cost_header=part #cost header name
    make_transaction_objects(file_dictionary, merchant_header, cost_header)
       
#pass the whole file_dictionary to search merchant and make objects there
    """for row in file_dictionary:
        cost_as_string =row.get(cost_header)
       
        merchant_cost_dict = {row.get(merchant_header) : float(cost_as_string)}
        merchant_cost_list.append(merchant_cost_dict) 
    search_merchant(merchant_cost_list)  """ 

        

def make_transaction_objects(file_dictionary, merchant_header, cost_header):

    for row in file_dictionary:
        merchant_name = row.get(merchant_header)
        cost_as_string = row.get(cost_header)
        cost_as_float = float(cost_as_string)
        merchant_identifier = yelp_search(merchant_name)
        category = ollama_search(merchant_identifier)
        

        
def ollama_search(merchant_identifier):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",

        "prompt": f"""Which category does {merchant_identifier} belong to: GROCERY = "Groceries"
        RESTAURANTS = "Food & Drink"
        ENTERTAINMENT = "Entertainment"
        UTILITIES = "Housing & Utilities"
        TRANSPORTATION = "Transportation"
        ACADEMICS = "Academics and Supplies"
        PERSONAL_CARE = "Health &Personal Care"
        CLOTHING = "Clothing & Accessories"
        RETAIL = "Shopping & Retail"
        OTHER = "Other"? Just return the category name""",
        "stream": False
    }
    response = requests.post(url, json = data)
    category = response.json()["response"]
    return category

def yelp_search(merchant_name):
    headers = {
             "Authorization": f"Bearer {yelp_api_key}"
        }
    yelp_url = "https://api.yelp.com/v3/businesses/search"
    params = {
            "term": merchant_name,
            "location": "United States",
            "limit": 1
    }
    response = requests.get(yelp_url, headers=headers, params=params)
    data= response.json()
    merchant_identifier = data["businesses"][0]["categories"][0].get("alias")    
    return merchant_identifier
        