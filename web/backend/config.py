import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Required for session management
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/complaints_db")
    DEBUG = True