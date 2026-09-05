def test_evaluate_emergency_manual_sos(client, auth_headers):
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "trigger_type": "MANUAL",
        "gps_accuracy": 5.0,
        "battery_level": 80
    }
    response = client.post("/api/v1/emergency/evaluate", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "CRITICAL"
    assert data["requires_guardian_alert"] is True
    assert data["confidence"] > 0.90

def test_evaluate_emergency_shake_sensor(client, auth_headers):
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "trigger_type": "SHAKE",
        "gps_accuracy": 15.0,
        "battery_level": 12,
        "is_charging": False
    }
    response = client.post("/api/v1/emergency/evaluate", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "HIGH"
    assert data["requires_guardian_alert"] is True
    assert "Low battery" in data["recommended_action"]

def test_evaluate_emergency_normal(client, auth_headers):
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "trigger_type": "STANDBY",
        "gps_accuracy": 10.0,
        "threat_density": 0.0
    }
    response = client.post("/api/v1/emergency/evaluate", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "NORMAL"
    assert data["requires_guardian_alert"] is False
