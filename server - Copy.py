# possible python backend
from flask import Flask, request, jsonify
from flask_cors import CORS
from mjrp_implementation import main

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    # Extract parameters from JSON data
    # Call your main function with the parameters
    result = main(data['parameters'])
    return jsonify(result=result)

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


if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)