from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Guardian AI"
    assert data["status"] == "running"
    assert "health_check" in data

def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Guardian AI API"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data
    assert "disclaimer" in data
