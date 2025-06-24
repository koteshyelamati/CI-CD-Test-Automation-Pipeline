import pytest
from app.main import app as flask_app # Import your Flask app instance

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # You might need to configure your app for testing, e.g., TESTING = True
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert "Service is up and running!" in json_data["message"]

def test_mock_data_endpoint(client):
    """Test the /mock-data endpoint."""
    response = client.get('/mock-data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["id"] == 1
    assert json_data["name"] == "Sample Item"
    assert "version" in json_data["details"]

def test_mock_data_structure(client):
    """Test the structure of the /mock-data response."""
    response = client.get('/mock-data')
    assert response.status_code == 200
    json_data = response.get_json()

    expected_keys = ["id", "name", "value", "details"]
    for key in expected_keys:
        assert key in json_data, f"Key '{key}' missing in mock_data response"

    expected_details_keys = ["version", "author"]
    for key in expected_details_keys:
        assert key in json_data["details"], f"Key '{key}' missing in mock_data.details response"

# Example of a test for an edge case (e.g., a non-existent route)
def test_not_found_error(client):
    """Test a non-existent route to ensure it returns 404."""
    response = client.get('/non-existent-route')
    assert response.status_code == 404

# Example of a test that could be made to fail for demonstration
# def test_intentional_failure(client):
#     """This test is designed to fail for CI/CD demonstration purposes."""
#     response = client.get('/health')
#     assert response.status_code == 201 # Intentionally wrong status code
#     assert False, "This test is intentionally failing."
