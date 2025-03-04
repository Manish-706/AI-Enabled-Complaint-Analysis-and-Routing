from flask import Flask
from flask_socketio import SocketIO
from .config import Config
from .routes.home_routes import home_routes
from .routes.department_routes import department_routes
from .routes.map_routes import map_routes
from .routes.auth_routes import auth_routes
import schedule
import time
import threading
from src.data_collection.webScrapping import scrape_data
import os

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.abspath("../../web/backend/templates"))

# Apply configuration from Config class
app.config.from_object(Config)

# Initialize SocketIO
socketio = SocketIO(app)

# Register Blueprints
app.register_blueprint(home_routes)
app.register_blueprint(department_routes)
app.register_blueprint(map_routes)
app.register_blueprint(auth_routes)

# Function to run the scheduler
def run_scheduler():
    # Schedule the scraping function to run every 5 minutes
    schedule.every(5).minutes.do(scrape_data)
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True  # Daemonize the thread so it stops when the main program stops
print("Starting scheduler thread...")
scheduler_thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True)