
from pymongo.mongo_client import MongoClient
from pymongo import errors
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGO_URI")

client = MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=True,
)


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.fruits_application

collection_name = db["fruits_app"]

def check_mongo_connection():
    """ Function to test the MongoDB connection
    """
    try:
        client.admin.command('ping')
        return {"status": "ok"}
    except errors.ServerSelectionTimeoutError:
        return {"status": "error", "detail": "MongoDB server selection timeout"}
    except errors.ConnectionFailure:
        return {"status": "error", "detail": "MongoDB connection failure"}
    except Exception as e:
        return {"status": "error", "detail": f"Unexpected error: {str(e)}"}