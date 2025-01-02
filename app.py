from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_required, current_user
import random
import time
import threading
from login import login_blueprint, init_login_manager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Initialize Flask-Login
init_login_manager(app)

# Register login blueprint
app.register_blueprint(login_blueprint)

# Toggle to switch between live and dummy data
USE_DUMMY_DATA = True

# Dummy GPS coordinates for 10 cars
dummy_cars_data = {
    "car_1": [23.8103, 90.4125],
    "car_2": [22.3475, 91.8123],
    "car_3": [24.3636, 88.6241],
    "car_4": [22.8456, 89.5403],
    "car_5": [24.8949, 91.8687],
    "car_6": [23.9985, 90.4203],
    "car_7": [24.7520, 90.4033],
    "car_8": [22.7022, 90.3493],
    "car_9": [25.7439, 89.2565],
    "car_10": [22.3240, 91.8325]
}

def simulate_dummy_movement():
    while USE_DUMMY_DATA:
        for car_id in dummy_cars_data:
            lat, lng = dummy_cars_data[car_id]
            # Very small random movements to simulate realistic car behavior
            lat += random.uniform(-0.0001, 0.0001)
            lng += random.uniform(-0.0001, 0.0001)
            dummy_cars_data[car_id] = [lat, lng]
        time.sleep(0.5)  # Update every 0.5 seconds for smoother simulation

# Start simulation in the background
if USE_DUMMY_DATA:
    threading.Thread(target=simulate_dummy_movement, daemon=True).start()

@app.route('/')
@login_required
def home():
    return render_template('index.html', username=current_user.id)

@app.route('/map')
@login_required
def map_view():
    return render_template('map.html')

@app.route('/get_cars_data', methods=['GET'])
@login_required
def get_cars_data():
    if USE_DUMMY_DATA:
        return jsonify(dummy_cars_data)
    else:
        return jsonify({})  # Placeholder if live data is disabled

if __name__ == '__main__':
    app.run(debug=True)
