from datetime import datetime, timezone
from app.schemas.location import LocationCreateRequest

def test_record_location_success(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="location_user@example.com")
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "accuracy": 4.5
    }
    response = client.post("/api/v1/locations", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["latitude"] == 37.7749
    assert data["longitude"] == -122.4194
    assert data["accuracy"] == 4.5
    assert "timestamp" in data

def test_record_location_invalid_latitude(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="bad_lat@example.com")
    payload = {
        "latitude": 105.0,  # Invalid: > 90
        "longitude": -122.4194,
        "accuracy": 5.0
    }
    response = client.post("/api/v1/locations", json=payload, headers=headers)
    assert response.status_code == 422

def test_record_location_invalid_longitude(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="bad_lon@example.com")
    payload = {
        "latitude": 37.7749,
        "longitude": -200.0,  # Invalid: < -180
        "accuracy": 5.0
    }
    response = client.post("/api/v1/locations", json=payload, headers=headers)
    assert response.status_code == 422

def test_record_location_unauthorized(client):
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "accuracy": 5.0
    }
    response = client.post("/api/v1/locations", json=payload)
    assert response.status_code in [401, 403]

def test_record_location_batch_success(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="batch_user@example.com")
    payload = {
        "locations": [
            {"latitude": 37.7749, "longitude": -122.4194, "accuracy": 5.0},
            {"latitude": 37.7800, "longitude": -122.4100, "accuracy": 4.0}
        ]
    }
    response = client.post("/api/v1/locations/batch", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["processed_count"] == 2
    assert data["ignored_duplicates_count"] == 0
    assert len(data["items"]) == 2

def test_record_location_batch_server_deduplication(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="dedup_user@example.com")
    now_iso = datetime.now(timezone.utc).isoformat()
    # Batch containing identical point twice within 2 seconds
    payload = {
        "locations": [
            {"latitude": 37.7749, "longitude": -122.4194, "accuracy": 5.0, "timestamp": now_iso},
            {"latitude": 37.7749, "longitude": -122.4194, "accuracy": 5.0, "timestamp": now_iso}
        ]
    }
    response = client.post("/api/v1/locations/batch", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["processed_count"] == 1
    assert data["ignored_duplicates_count"] == 1
