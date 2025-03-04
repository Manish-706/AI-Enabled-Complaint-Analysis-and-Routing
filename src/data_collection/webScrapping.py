# scraper.py
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
from pymongo import MongoClient
from src.preprocessing.preprocess import preprocess_text
from src.trained_model.predict import predict_complaint_category


# MongoDB Connection
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["complaints_db"]
    return db

# Function to scrape data from MyGov website
def scrape_data():
    print("Scraping data...")
    try:
        service = Service("C:\Windows\chromedriver.exe")  # Ensure the correct path
        driver = webdriver.Chrome(service=service)
        driver.get("https://mygov-zeta.vercel.app/")
        
        time.sleep(5)  # Wait for JavaScript to load the data

        rows = driver.find_elements(By.XPATH, "//table[@id='complaintTable']/tbody/tr")
        
        db = get_db()
        scraped_collection = db["scraped_complaints"]
        categorized_collection = db["categorized_complaints"]
        
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) == 4:
                complaint_id = columns[0].text
                Complaint = columns[1].text
                location = columns[2].text
                source = columns[3].text

                extracted_data = {
                "complaint_id" : complaint_id,
                "Complaint" : Complaint,
                "location" : location,
                "source" :source,
                "timestamp": datetime.now()
                }

                scraped_collection.insert_one(extracted_data)
                print(f"Scraped data Stored: {Complaint}")
                


                # Clean the Complaint text
                cleaned_text = preprocess_text(Complaint)
            
                # Predict category and assign department 
                category, department = predict_complaint_category(cleaned_text)
              
                # complaints with predicted category
                complaint_data = {
                    "complaint_id": complaint_id,
                    "Complaint": Complaint,
                    "location": location,
                    "source": source,
                    "status": "Pending",
                    "category": category,
                    "department": department,
                    "timestamp": datetime.now()
                }
                categorized_collection.insert_one(complaint_data)
                print(f"Categorized data Stored: {Complaint}")
        
        driver.quit()
    except Exception as e:
        print(f"Error during scraping: {e}")
