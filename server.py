from flask import Flask, request, jsonify,render_template, send_from_directory
from flask_cors import CORS
from mjrp import calculate_cost
import os
import json

app = Flask(__name__)

app = Flask(__name__, static_folder='C:/Users/Dell/UsersDellSAAFRT/static')

# server.py

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    print(data)
    if not data or 'parameters' not in data:
        return jsonify({"error": "No JSON data provided"}), 400

    parameters = data['parameters']
    print(parameters)
    # Extract all parameters into a dictionary
    extracted_params = {}
    for param in parameters:
        param_name = param['name']
        param_value = param['value']
        # Ensure param_value is always a list
        if not isinstance(param_value, list):
            param_value = [param_value]  # Convert single value to list
        extracted_params[param_name] = param_value

    # Call the calculate_cost function with the extracted parameters
    print(extracted_params)
    result = calculate_cost(extracted_params)

    return jsonify(result), 200




# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Serve index.html for root URL
@app.route('/')
def index():
    return render_template('index.html')

#for the graphical user interfaces

# for testing purposes only
@app.route('/dummy', methods=['GET'])
def dummy_endpoint():
    dummy_data = {
        'message': 'This is a dummy JSON response for testing purposes.',
        'data': {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }
    }
    return jsonify(dummy_data)

# Enable CORS for all routes
CORS(app)

if __name__ == '__main__':
    # Production Deployment
    app.run(host='0.0.0.0', port=5000)  # Use appropriate port for production
