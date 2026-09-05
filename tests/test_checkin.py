from fastapi.testclient import TestClient

def test_checkin_lifecycle(client: TestClient, auth_headers: dict):
    # 1. Start Check-in
    start_resp = client.post(
        "/api/v1/checkin/start",
        headers=auth_headers,
        json={"duration_minutes": 30, "destination": "Home", "note": "Walking home"}
    )
    assert start_resp.status_code == 201
    start_data = start_resp.json()
    assert start_data["status"] == "ACTIVE"
    assert start_data["duration_minutes"] == 30

    # 2. Get Status
    status_resp = client.get(
        "/api/v1/checkin/status",
        headers=auth_headers
    )
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "ACTIVE"

    # 3. Check in as Safe
    safe_resp = client.post(
        "/api/v1/checkin/safe",
        headers=auth_headers
    )
    assert safe_resp.status_code == 200
    assert safe_resp.json()["status"] == "SAFE"
