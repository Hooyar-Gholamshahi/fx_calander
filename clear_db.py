from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv(find_dotenv())
password = os.environ.get("mongo_pwd")

# اتصال به MongoDB
connection_string = f"mongodb+srv://hooyargholamshahibiz:{password}@poseidon.grrgsbp.mongodb.net/?retryWrites=true&w=majority&appName=Poseidon"
client = MongoClient(connection_string)
db = client.fxstreet_db  # نام دیتابیس دلخواه
collection = db.fx_calendar  # نام کالکشن دلخواه
collection = db.large_db  # نام کالکشن دلخواه

# # حذف اولین داکیومنتی که match بشه
# result = collection.delete_one({"customer": "Ali"})
# print("Deleted:", result.deleted_count)

# # حذف همه‌ی داکیومنت‌های cancel شده
# result = collection.delete_many({"status": "canceled"})
# print("Deleted:", result.deleted_count)

# حذف کل اسناد (خالی کردن collection)
result = collection.delete_many({})
print("Deleted:", result.deleted_count)
