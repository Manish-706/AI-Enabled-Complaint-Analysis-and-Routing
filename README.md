# 🚀 AI-Enabled Public Service Complaint Analysis & Routing
# Hackathon Project

An AI-powered system to automate the **collection**, **classification**, and **routing** of citizen complaints from various sources like government portals and social media. It improves public service delivery by ensuring efficient and timely complaint resolution.

---

## 📌 Purpose
To streamline public complaint management using **Machine Learning** and **Real-time Visualization**, enabling government departments to address citizen issues promptly.

---

## 🛠️ Tech Stack
- **Backend:** Flask, Flask-SocketIO
- **Frontend:** HTML, CSS, JavaScript, Chart.js, Leaflet.js
- **Machine Learning:** Scikit-learn (KMeans), NLTK
- **Database:** MongoDB
- **Web Scraping:** Selenium
- **Real-Time Updates:** WebSockets, SocketIO

---

## 🎯 Key Features
1. Automated **Web Scraping** of complaints (every 5 minutes)
2. **Text Cleaning & Preprocessing** using NLP (NLTK)
3. **Complaint Categorization** with KMeans Clustering
4. Automatic **Department Routing**
5. **Real-Time Complaint Updates** via WebSockets
6. Interactive **Dashboard with Charts and Maps**
7. Department **Login & Complaint Management System**

---

## 🏢 Complaint Categories
- Water Issues
- Electricity Issues
- Road Maintenance
- Sanitation
- Public Works
- Transport
- Health & Medical Services
- Anti-Corruption
- Education
- Urban Development

---

## ⚙️ How It Works
1. **Scrape complaints** → store in `scraped_complaints`
2. **Clean & categorize** → store in `categorized_complaints`
3. **Assign to departments** based on category
4. **Display on frontend** using real-time SocketIO events and REST APIs

---

## 🚀 Getting Started
### Prerequisites
- Python 3.9+
- MongoDB
- ChromeDriver (for Selenium)

### Installation
```bash
git clone https://github.com/yourusername/finalProject.git
cd finalProject
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
