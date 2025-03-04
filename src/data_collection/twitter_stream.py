import tweepy
import json
from pymongo import MongoClient

# Twitter API Credentials (Replace with actual credentials)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

# MongoDB Connection
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["complaints_db"]
    return db

# Tweepy Stream Listener
class ComplaintStreamListener(tweepy.StreamingClient):
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if "text" in data:
            complaint_text = data["text"]
            complaint = {"text": complaint_text, "source": "Twitter", "status": "Pending"}
            db = get_db()
            db["scraped_complaints"].insert_one(complaint)
            print("Stored Complaint:", complaint_text)

    def on_error(self, status_code):
        print("Error:", status_code)
        return False  # Stop streaming on error

# Start Streaming
def start_streaming():
    stream = ComplaintStreamListener(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    stream.filter(track=["complaint", "issue", "problem"], languages=["en"])

if __name__ == "__main__":
    start_streaming()
