from flask import Flask, jsonify, render_template
import os
import json
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from log_config import logger

load_dotenv()
base_dir = os.getenv("BASE_DIR")

app = Flask(__name__)
socketio = SocketIO(app)


# ------------------------------
# Functions to be used
# ------------------------------

def read_stock_data():
    file_path = os.path.join(base_dir, "data/stock_data.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    return {"error": "Data not found"}

def read_sensor_data():
    file_path = os.path.join(base_dir, "data/sensor_data.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    logger.warning("Sensor data file not found")
    return {"error": "Data not found"}

def read_cvbankas_data():
    file_path = os.path.join(base_dir, "data/cvbankas_ads.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            if 'jobs' in data and isinstance(data['jobs'], list):
                data['jobs'] = data['jobs'][:9]  # Limit to 6 jobs
            return data
    return {"error": "Data not found"}

def read_system_info():
    file_path = os.path.join(base_dir, "data/system_info.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    return {"error": "Data not found"}

def read_random_quote():
    file_path = os.path.join(base_dir, "data/random_quote.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    return {"error": "Data not found"}

def read_rescuetime_data():
    file_path = os.path.join(base_dir, "data/rescuetime_data.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    return {"error": "Data not found or invalid format"}

# SocketIO Event Handlers (BACKEND, SERVER)
# Listening for incoming connections such as `request_from_client_to_server_for_stock_data`
# and sending back the data(that we received over `read_stock_data`) 
# to the client over `response_from_server_to_client_with_stock_data`

@socketio.on('connect')
def event_handler_connect():
    """
    Event handler for client connection.
    When a client connects, it sends initial data for all components.
    """
    emit('response_from_server_to_client_with_stock_data', read_stock_data())
    emit('response_from_server_to_client_with_cvbankas_data', read_cvbankas_data())
    emit('response_from_server_to_client_with_sensor_data', read_sensor_data())
    emit('response_from_server_to_client_with_rescuetime_data', read_rescuetime_data())

@socketio.on('request_from_client_to_server_for_stock_data')
def event_handler_stock():
    emit('response_from_server_to_client_with_stock_data', read_stock_data())

@socketio.on('request_from_client_to_server_for_sensor_data')
def event_handler_sensor():
    emit('response_from_server_to_client_with_sensor_data', read_sensor_data())

@socketio.on('request_from_client_to_server_for_cvbankas_data')
def event_handler_cvbankas():
    emit('response_from_server_to_client_with_cvbankas_data', read_cvbankas_data())

@socketio.on('request_from_client_to_server_for_system_info_data')
def event_handler_system_info():
    emit('response_from_server_to_client_with_system_info_data', read_system_info())

@socketio.on('request_from_client_to_server_for_random_quote_data')
def event_handler_random_quote():
    emit('response_from_server_to_client_with_quote_data', read_random_quote())

@socketio.on('request_from_client_to_server_for_rescuetime_data')
def event_handler_rescuetime():
    emit('response_from_server_to_client_with_rescuetime_data', read_rescuetime_data())

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # Run the Flask application with SocketIO
    socketio.run(
        app, 
        debug=True, 
        host='0.0.0.0', 
        port=5000, # sudo lsof -i :5000 and sudo kill -9 PID
        allow_unsafe_werkzeug=True # so could run as a service
    )
