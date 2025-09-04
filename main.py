from dotenv import load_dotenv , find_dotenv
load_dotenv(find_dotenv())
import os
import pprint
from pymongo import MongoClient

password = os.environ.get("mongo_pwd")

conection_string = f"mongodb+srv://hooyargholamshahibiz:{password}@poseidon.grrgsbp.mongodb.net/?retryWrites=true&w=majority&appName=Poseidon"

client = MongoClient(conection_string)

dbs = client.list_database_names()
test_dbs = client.test
collections = test_dbs.list_collection_names()
print(client.sample_mflix)


