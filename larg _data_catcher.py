import time
from pymongo import MongoClient,ASCENDING, DESCENDING
from datetime import datetime
import pprint  # برای پرینت خوشگل‌تر




# اتصال به سرور Atlas
uri = "mongodb+srv://hooyargholamshahibiz:fjsGbz346d0mCmDo@poseidon.grrgsbp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

# اتصال به دیتابیس
db = client["fxstreet_db"]
collection = db["large_db"]


#------------filter------------


#-------time-------

start = input("past :" )
end   = input("now :" )

# ---country/currency---

country_map = { # currency_map
    "AUD": "AUD", "AU": "AUD",#
    "CAD": "CAD", "CA": "CAD",#
    "CHF": "CHF", "CH": "CHF", #
    "CNY": "CNY", "CN": "CNY", #
    "EUR": "EUR", "DE": "EUR",# "EU" : "EU"
    "FR" : "EUR", "IT": "EUR",
    "ES": "EUR",
    "AUD":"AUD" , "AU" : "AUD",
    "NZD": "NZD", "NZ": "NZD",#
    "GBP": "GBP", "GB": "GBP",
    "JPY": "JPY", "JP": "JPY",
    "USD": "USD", "US" : "USD",
}

country = []
while True:
    cc = input("select country/currenc or (quit) : ").upper()
    
    if cc in country_map:
        country.append(country_map[cc])
        print("Selected code:", country)
    elif cc == "QUIT":
        break
    else:
        print("wrong, try again.")
        pass


#---volatilities---

volatilities_map = { "NONE" : "NONE" ,
                     "LOW" : "LOW" , 
                     "MEDIUM" : "MEDIUM" , 
                     "HIGH" : "HIGH" }

volatilities = []
while True:
    cc = input("select volatilities or (quit) : ").upper()
    
    if cc in volatilities_map:
        volatilities.append(volatilities_map[cc])
        print("Selected code:", volatilities)
    elif cc == "QUIT":
        break
    else:
        print("wrong, try again.")
        pass



#---time---

rc_start = time.time()


collection.create_index([
    ("currencyCode", 1),
    ("volatility", 1),
    ("dateUtc", 1),
])


query = {}
if country:  
    query["currencyCode"] = {"$in": country}
if volatilities:  
    query["volatility"] = {"$in": volatilities}
if start and end:
    query["dateUtc"] = {"$gte": start, "$lte": end}




cursor = collection.find(query , {
                                  "dateUtc": 1,
                                  "name" : 1,
                                  "currencyCode": 1,
                                  "volatility": 1,
                                  "_id": 0
                                  })
count = collection.count_documents(query)

rc_end = time.time()


for doc in cursor:
    pprint.pprint(doc)

print("matched docs: ",count)


print("with index : " , rc_end-rc_start)
print(start)
print(end)







