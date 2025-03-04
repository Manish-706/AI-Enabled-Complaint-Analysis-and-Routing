import sys
import os

# Get the absolute path of the project root (finalProject)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, BASE_DIR)  # Add root directory to sys.path

from datetime import datetime, timedelta
from collections import defaultdict
from flask import Blueprint, render_template, jsonify
from flask_socketio import SocketIO
from src.database.database import fetch_piechart_data, get_complaints

# Initialize Blueprint
home_routes = Blueprint('home_routes', __name__)

# Initialize SocketIO (ensure this is the same instance used in app.py)
socketio = SocketIO()

# Route for rendering the home page
@home_routes.route('/home')
def home():
    return render_template('index.html')

# WebSocket event for real-time updates
@socketio.on('request_complaints')
def send_complaints():
    complaints = get_complaints()
    socketio.emit('update_complaints', complaints)

# Route for fetching pie chart data dynamically
@home_routes.route('/home/<category>')
def pie_chart(category):
    data = fetch_piechart_data(category)
    # Format data for Chart.js
    formatted_data = [data.get('Pending', 0), data.get('Resolved', 0), data.get('In Progress', 0)]
    return jsonify(formatted_data)

# Route for fetching complaint chart data dynamically
@home_routes.route('/home/get_complaint_chart')
def get_complaint_chart():
    complaints = get_complaints()
    
    # Get the current time and the time 5 minutes ago
    now = datetime.now()
    five_minutes_ago = now - timedelta(minutes=5)
    
    # Filter complaints received in the last 5 minutes
    recent_complaints = [
        complaint for complaint in complaints
        if 'timestamp' in complaint and complaint['timestamp'] >= five_minutes_ago
    ]
    
    # Count the number of complaints in the last 5 minutes
    complaint_count = len(recent_complaints)
    
    # Prepare data for the chart
    labels = [now.strftime('%H:%M')]  # Current time as the label
    values = [complaint_count]  # Number of complaints in the last 5 minutes
    
    return jsonify({"labels": labels, "values": values})