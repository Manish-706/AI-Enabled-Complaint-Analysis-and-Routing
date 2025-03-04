from flask import Blueprint, render_template, request, redirect, url_for, session
from src.database.database import get_user, create_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Blueprint
auth_routes = Blueprint('auth_routes', __name__)

# Route for rendering the login page
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['department'] = user['department']
            # Redirect to the complaint list page after successful login
            return redirect(url_for('department_routes.department_complaints', department_name=user['department']))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

# Route for rendering the registration page
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        department = request.form['department']

        # Check if the user already exists
        if get_user(username):
            return render_template('register.html', error='Username already exists')

        # Create the user
        create_user(username, password, department)
        session['user'] = username
        session['department'] = department
        # Redirect to the complaint list page after successful registration
        return redirect(url_for('department_routes.department_complaints', department_name=department))

    return render_template('register.html')

# Route for logging out
@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_routes.login'))