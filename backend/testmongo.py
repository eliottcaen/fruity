from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()
uri = os.getenv("MONGO_URI")

client = MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=True,
)

print(1)
try:
    client.server_info()
    print("✅ Connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)
