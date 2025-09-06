import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not set")

client = MongoClient(MONGO_URI)
db = client["ecofinds"]  # database name

users = db["users"]
products = db["products"]
carts = db["carts"]
purchases = db["purchases"]

# Helpful indexes (run safely on every start)
users.create_index([("email", ASCENDING)], unique=True)
products.create_index([("title", ASCENDING)])
products.create_index([("category", ASCENDING)])
carts.create_index([("user_email", ASCENDING)])
purchases.create_index([("user_email", ASCENDING)])
