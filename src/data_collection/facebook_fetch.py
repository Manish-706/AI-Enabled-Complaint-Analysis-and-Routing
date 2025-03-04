import requests
import json
import schedule
import time
from pymongo import MongoClient

# Facebook API Credentials (Replace with actual credentials)
ACCESS_TOKEN = "your_facebook_access_token"
PAGE_ID = "your_page_id"
FB_GRAPH_URL = f"https://graph.facebook.com/v12.0/{PAGE_ID}/posts?access_token={ACCESS_TOKEN}"

# MongoDB Connection
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["complaints_db"]
    return db

# Fetch Facebook Complaints
def fetch_facebook_complaints():
    response = requests.get(FB_GRAPH_URL)
    if response.status_code == 200:
        posts = response.json().get("data", [])
        db = get_db()
        for post in posts:
            complaint_text = post.get("message", "")
            if complaint_text:
                complaint = {"text": complaint_text, "source": "Facebook", "status": "Pending"}
                db["scraped_complaints"].insert_one(complaint)
                print("Stored Complaint:", complaint_text)
    else:
        print("Failed to fetch Facebook data. Status Code:", response.status_code)

# Schedule fetching every 30 minutes
schedule.every(30).minutes.do(fetch_facebook_complaints)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
