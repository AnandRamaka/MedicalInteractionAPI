import csv
from pymongo import MongoClient

localhost_link = "localhost:27017"

client = MongoClient(localhost_link)

db = client['DrugID_NameMap']
collection = db['drug_map']

ids_to_synonyms = {}
synonyms_to_ids = {}

docs = []

with open("./synonyms.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:  
    drug_id = row[0]
    synonyms = row[1:]
    ids_to_synonyms[drug_id] = synonyms
    for s in synonyms:
      docs.append( { "synonym" : s, "drug_id" : drug_id } )

collection.insert_many(docs)