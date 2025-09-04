# url = "https://calendar-api.fxsstatic.com/en/api/v2/eventDates/2025-08-17T00:00:00Z/2025-08-23T23:59:59Z?&volatilities=NONE&volatilities=LOW&volatilities=MEDIUM&volatilities=HIGH&countries=US&countries=UK&countries=EMU&countries=DE&countries=CN&countries=JP&countries=CA&countries=AU&countries=NZ&countries=CH&countries=FR&countries=IT&countries=ES&countries=UA&categories=8896AA26-A50C-4F8B-AA11-8B3FCCDA1DFD&categories=FA6570F6-E494-4563-A363-00D0F2ABEC37&categories=C94405B5-5F85-4397-AB11-002A481C4B92&categories=E229C890-80FC-40F3-B6F4-B658F3A02635&categories=24127F3B-EDCE-4DC4-AFDF-0B3BD8A964BE&categories=DD332FD3-6996-41BE-8C41-33F277074FA7&categories=7DFAEF86-C3FE-4E76-9421-8958CC2F9A0D&categories=1E06A304-FAC6-440C-9CED-9225A6277A55&categories=33303F5E-1E3C-4016-AB2D-AC87E98F57CA&categories=9C4A731A-D993-4D55-89F3-DC707CC1D596&categories=91DA97BD-D94A-4CE8-A02B-B96EE2944E4C&categories=E9E957EC-2927-4A77-AE0C-F5E4B5807C16"


import asyncio
import httpx
import json
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv



#-------DataBase Connection-------


# بارگذاری متغیرهای محیطی
load_dotenv(find_dotenv())
password = os.environ.get("mongo_pwd")

# اتصال به MongoDB
connection_string = f"mongodb+srv://hooyargholamshahibiz:{password}@poseidon.grrgsbp.mongodb.net/?retryWrites=true&w=majority&appName=Poseidon"
client = MongoClient(connection_string)
db = client.fxstreet_db  # نام دیتابیس دلخواه
collection = db.large_db  # نام کالکشن دلخواه


#-----------filter-----------

#---------defult time--------------

# defult time : Thu, Aug 1st, 2024
# defult time : Sun, Aug 31st, 2025(now)

#-----------Time-----------

# # time 
# from_now = datetime.now(timezone.utc) # - timedelta(hours=1)
# to_then = from_now + timedelta(days=10) 
# # برای پارامتر days یک متغیر تعریف کن تا از کاربر دریافت بشه
# # حواست باشه همیشه باید 

# now_str = from_now.strftime("%Y-%m-%dT%H:%M:%SZ")
# before_str = to_then.strftime("%Y-%m-%dT%H:%M:%SZ")

# print("Now:", now_str)
# print("Before:", before_str)

from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0,microsecond=0)

x = int(input("deltime : "))

timedel = timedelta(days=x)

date_from = today
date_to = today - timedel

# تبدیل به رشته RFC 3339
# date_from_str = date_from.strftime("%Y-%m-%dT%H:%M:%S")
# date_to_str = date_to.strftime("%Y-%m-%dT%H:%M:%S")
date_from_str = date_from.strftime("%Y-%m-%dT%H:%M:%SZ")
date_to_str = date_to.strftime("%Y-%m-%dT%H:%M:%SZ")

print(date_from_str)  # مثل: 2025-08-21T00:00:00Z
print(date_to_str)    # مثل: 2025-08-31T00:00:00Z
print(date_from_str < date_to_str)
"%Y-%m-%dT%H:%M:%S"

# YYYY-MM-DDTHH:MM:SS.mmmZ
#----------Data request function----------



async def main():
    # url = f"https://calendar-api.fxsstatic.com/en/api/v2/eventDates/{now_str}/{before_str}"

    if date_from_str > date_to_str :
        url = f"https://calendar-api.fxsstatic.com/en/api/v2/eventDates/{date_to_str}/{date_from_str}"
    else :
        url = f"https://calendar-api.fxsstatic.com/en/api/v2/eventDates/{date_from_str}/{date_to_str}"

    headers = {"Referer": "https://www.fxstreet.com/"}

    async with httpx.AsyncClient(timeout=30.0) as client_http:
        response = await client_http.get(url, headers=headers) # params={"countries" : country} 
        print("Status code:", response.status_code, response.url)

        data = response.json()
        # print(json.dumps(data, indent=4, ensure_ascii=False))

        # اضافه کردن timestamp ذخیره
        # document = {
        #     "fetched_at": date_from_str,
        #     "event": data
        # }

        # print(document)
        # ذخیره در MongoDB
        # result = collection.insert_one(document)
        result = collection.insert_many(data)
        # print("Inserted document ID:", result.inserted_id)

asyncio.run(main())

