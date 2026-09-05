from fastapi.testclient import TestClient

def test_get_nearby_safe_places(client: TestClient, auth_headers: dict):
    response = client.get(
        "/api/v1/locations/safe-places?latitude=37.7749&longitude=-122.4194",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_found" in data
    assert len(data["places"]) > 0
    assert data["places"][0]["category"] in ["POLICE", "HOSPITAL", "FIRE_STATION", "SHELTER"]
