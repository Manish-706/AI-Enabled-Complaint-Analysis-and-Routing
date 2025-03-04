from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from src.database.database import get_complaints_by_department

# Initialize Blueprint
department_routes = Blueprint('department_routes', __name__)

# Route for rendering department selection page
@department_routes.route('/department')
def department_home():
    return render_template('departments.html')

# Route for handling department-specific complaints
@department_routes.route('/department/<department_name>')
def department_complaints(department_name):
    if 'user' in session and session.get('department') == department_name:
        return render_template('list.html')
    return redirect(url_for('department_routes.department_home'))

# API endpoint to fetch complaints for a department
@department_routes.route('/department/<department_name>/complaints')
def get_department_complaints_api(department_name):
    # if 'user' in session and session.get('department') == department_name:
        complaints = get_complaints_by_department(department_name)
        return jsonify(complaints)
    # return jsonify({"error": "Unauthorized"}), 401