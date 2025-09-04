from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv
from bson import ObjectId
import pprint
import time

load_dotenv(find_dotenv())
password = os.environ.get("mongo_pwd")

# اتصال به MongoDB
connection_string = f"mongodb+srv://hooyargholamshahibiz:{password}@poseidon.grrgsbp.mongodb.net/?retryWrites=true&w=majority&appName=Poseidon"
client = MongoClient(connection_string)
db = client.fxstreet_db  # نام دیتابیس دلخواه
collection = db.fx_calendar  # نام کالکشن دلخواه


# print(type(collection))

# data = collection.find({},{"events"})

# c = collection.count_documents({"events.events": {"$exists": True}})
# print(c)

# for i in data:
#     pprint.pprint(i)

# pipeline = [
#     {"$project": {"count": {"$size": "$events"}}}
#     {"$project": {"count": {"$size": "$events"}}}
# ]

# for doc in collection.aggregate(pipeline):
#     print(doc["count"])


# pipeline = [
#     {"$unwind": "$events"},                 # باز کردن آرایه و تبدیل هر event به یک سند جدا
#     {"$project": {"event": "$events", "_id": 0}},  # انتخاب فقط محتوای هر event
# ]

start = time.time()

pipeline_match = [
        #    {"$match": {"_id": ObjectId("68ad4e9f50225e17900dc79a")}},  # انتخاب سند خاص
            {"$match": {}}  # انتخاب تمام سند ها
]

pipeline_project = [    
                    {"$project": {"events": 1, "_id": 0}}                       # نگه داشتن کل events
]

    
pipeline_mix = pipeline_match + pipeline_project 

cursor = collection.aggregate(pipeline_mix)


for doc in cursor:
    events = doc["events"]
    # pprint.pprint(doc)
    print("Count:", len(events))

end = time.time()

print(end-start)