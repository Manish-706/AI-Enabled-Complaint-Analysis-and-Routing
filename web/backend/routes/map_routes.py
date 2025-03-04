from flask import Blueprint, render_template, jsonify
from src.database.database import fetch_complaints_with_location

# Initialize Blueprint
map_routes = Blueprint('map_routes', __name__)

# Route for rendering the map page
@map_routes.route('/map')
def map_page():
    return render_template('map.html')

# Route for fetching complaint location data
@map_routes.route('/map/data')
def map_data():
    data = fetch_complaints_with_location()
    return jsonify(data)
