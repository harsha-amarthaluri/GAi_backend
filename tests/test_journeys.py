from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

def test_start_and_get_active_journey(client: TestClient, auth_headers: dict):
    eta = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    payload = {
        "origin_latitude": 37.7749,
        "origin_longitude": -122.4194,
        "destination_address": "Downtown Central Station",
        "destination_latitude": 37.7849,
        "destination_longitude": -122.4094,
        "expected_arrival_time": eta
    }

    # Start journey
    res = client.post("/api/v1/journeys/start", json=payload, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "ACTIVE"
    assert data["destination_address"] == "Downtown Central Station"
    journey_id = data["id"]

    # Get active journey
    active_res = client.get("/api/v1/journeys/active", headers=auth_headers)
    assert active_res.status_code == 200
    active_data = active_res.json()
    assert active_data["id"] == journey_id
    assert active_data["status"] == "ACTIVE"

def test_complete_journey(client: TestClient, auth_headers: dict):
    eta = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    payload = {
        "origin_latitude": 37.7749,
        "origin_longitude": -122.4194,
        "destination_address": "Home",
        "destination_latitude": 37.7849,
        "destination_longitude": -122.4094,
        "expected_arrival_time": eta
    }

    res = client.post("/api/v1/journeys/start", json=payload, headers=auth_headers)
    assert res.status_code == 201
    journey_id = res.json()["id"]

    complete_res = client.post(f"/api/v1/journeys/{journey_id}/complete", headers=auth_headers)
    assert complete_res.status_code == 200
    assert complete_res.json()["status"] == "COMPLETED"

    # Active journey should now be None
    active_res = client.get("/api/v1/journeys/active", headers=auth_headers)
    assert active_res.status_code == 200
    assert active_res.json() is None
