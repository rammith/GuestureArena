from pymongo import MongoClient
from app.core.config import settings


client = MongoClient(
    settings.MONGODB_URL,
    serverSelectionTimeoutMS=5000
)

database = client[settings.MONGODB_DATABASE]


def check_database_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")
        return True

    except Exception as error:
        print(f"MongoDB connection failed: {error}")
        return False


def close_database_connection():
    client.close()