from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns a JSON response indicating the service is healthy.
    """
    return jsonify({"status": "healthy", "message": "Service is up and running!"}), 200

@app.route('/mock-data', methods=['GET'])
def get_mock_data():
    """
    Mock data endpoint.
    Returns a sample JSON response.
    """
    mock_data = {
        "id": 1,
        "name": "Sample Item",
        "value": "This is some mock data.",
        "details": {
            "version": "1.0",
            "author": "AI Assistant"
        }
    }
    return jsonify(mock_data), 200

if __name__ == '__main__':
    # Note: For development only. In production, use a WSGI server like Gunicorn.
    app.run(host='0.0.0.0', port=5000, debug=True)
