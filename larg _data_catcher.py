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

# فرض کن اینا رو کاربر داده
start_input = input("past :" )
end_input   = input("now :" )

# تبدیل به datetime
start = datetime.strptime(start_input, "%Y-%m-%d")
end   = datetime.strptime(end_input, "%Y-%m-%d")

# تبدیل به string در فرمت ISO 8601 با Z
start_str = start.strftime("%Y-%m-%dT%H:%M:%SZ")
end_str   = end.strftime("%Y-%m-%dT%H:%M:%SZ")

print(start_str)  # 2024-07-01T00:00:00Z
print(end_str)    # 2025-08-30T00:00:00Z

#هی تو نیاز نیست اینجا یا هرجای دیگه ای فرمت تایم رو عوض کنی و دستکاریش کنی کافیه فقط بازرو بگیری محاسبه کنی چقدر بینشون فاصلست
# و در ادامه تام شروع رو بگیری و به اندازه فاصلش با تایم پایان همون مقدار بالا بری 

# 30 - 12 = 18
# 12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-30

# from pymongo import MongoClient
# from datetime import datetime, timezone

# client = MongoClient("mongodb://localhost:27017")
# db = client["mydatabase"]
# collection = db["mycollection"]

# start_dt = datetime(2025, 9, 3, 0, 0, 0, tzinfo=timezone.utc)
# end_dt = datetime(2025, 9, 5, 23, 59, 59, tzinfo=timezone.utc)

# query = {"dateUtc": {"$gte": start_dt, "$lte": end_dt}}
# results = collection.find(query)

# for doc in results:
#     print(doc)

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


# ---isScoreTrackable---

isScoreTrackable = []  # پیش‌فرض خالی

while True:
    cc = input("select isScoreTrackable (true/false) or (quit): ").lower()
    
    if cc == "quit":
        break
    elif cc == "true":
        isScoreTrackable.append(True)
    elif cc == "false":
        isScoreTrackable.append(False)
    else:
        print("wrong, try again.")
        

#---time---

rc_start = time.time()


collection.create_index([
    ("currencyCode", 1),
    ("volatility", 1),
    # ("isScoreTrackable",1),
    ("dateUtc", 1)
])


query = {}
if country:  
    query["currencyCode"] = {"$in": country}
if volatilities:  
    query["volatility"] = {"$in": volatilities}
# if isScoreTrackable:  
#     query["isScoreTrackable"] = {"$in": isScoreTrackable}
if start_input and end_input:
    query["dateUtc"] = {"$gte": start_str, "$lte": end_str}



cursor = collection.count_documents(query)

# cursor = collection.find(
#     {},  # شرط جستجو، {} یعنی همه
#     {"dateUtc": 1,"name" : 1,"currencyCode": 1, "volatility": 1, "_id": 0}  # projection
# )

for doc in collection.find({}, {"dateUtc": 1, "_id": 0}):
    print(doc["dateUtc"])


rc_end = time.time()

# for doc in cursor:
    # pprint.pprint(doc)


print("with index : " , rc_end-rc_start)











