from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# MongoDB Connection Setup
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["complaints_db"]
    return db

# User Operations
def create_user(username, password, department):
    db = get_db()
    user = {"username": username, "password": generate_password_hash(password), "department": department}
    db["users"].insert_one(user)
    return user

def get_user(username):
    db = get_db()
    return db["users"].find_one({"username": username})

# Complaint Operations
def create_complaint(Complaint, location, category, department, status="Pending"):
    db = get_db()
    complaint = {
        "Complaint": Complaint,
        "location": location,
        "category": category,
        "department": department,
        "status": status,
        "timestamp": datetime.now()  # Add a timestamp when the complaint is created
    }
    db["categorized_complaints"].insert_one(complaint)
    return complaint

def get_complaints():
    db = get_db()
    return list(db["categorized_complaints"].find({}, {"_id": 0}))

def get_complaints_by_department(department):
    db = get_db()
    return list(db["categorized_complaints"].find({"department": department}, {"_id": 0}))

def update_complaint_status(complaint_id, status):
    db = get_db()
    db["categorized_complaints"].update_one({"_id": ObjectId(complaint_id)}, {"$set": {"status": status}})

# Fetch complaints by category for pie chart updates
def fetch_piechart_data(category):
    db = get_db()
    pipeline = [
        {"$match": {"category": category}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    result = list(db["categorized_complaints"].aggregate(pipeline))
    
    # Transform the result into a dictionary
    status_counts = {"Pending": 0, "Resolved": 0, "In Progress": 0}
    for item in result:
        status = item["_id"]
        count = item["count"]
        status_counts[status] = count
    
    return status_counts

# Fetch complaints with location for map display
def fetch_complaints_with_location():
    db = get_db()
    complaints = list(db["categorized_complaints"].find({"location": {"$ne": None}}, {"_id": 0, "Complaint": 1, "location": 1, "status": 1, "category": 1}))
    
    # Filter out complaints with invalid or missing lat/lon values
    valid_complaints = []
    for complaint in complaints:
        if "location" in complaint and isinstance(complaint["location"], dict):
            lat = complaint["location"].get("lat")
            lon = complaint["location"].get("lon")
            if lat is not None and lon is not None:
                valid_complaints.append({
                    "Complaint": complaint["Complaint"],
                    "lat": lat,
                    "lon": lon,
                    "status": complaint["status"],
                    "category": complaint["category"]
                })
    
    return valid_complaints