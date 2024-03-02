from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from mjrp_implementation import main
import os

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    # Extract parameters from JSON data
    # Call your main function with the parameters
    result = main(data['parameters'])
    return jsonify(result=result)

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Serve index.html for root URL
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

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