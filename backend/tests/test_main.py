from fastapi.testclient import TestClient
from app.main import app

# Initialize the test client
client = TestClient(app)

def test_predict_endpoint():
    # Test with valid input
    response = client.post(
        "/predict/",
        json={"features": [0.5, 0.3, 0.2, 0.1, 0.4]}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()

    # Test with invalid input
    response = client.post(
        "/predict/",
        json={"features": "invalid"}
    )
    assert response.status_code == 400