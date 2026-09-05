def test_get_safety_score_success(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="safety_user@example.com")
    response = client.get("/api/v1/safety-score?latitude=37.7749&longitude=-122.4194", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "category" in data
    assert "location" in data
    assert data["location"]["latitude"] == 37.7749
    assert data["location"]["longitude"] == -122.4194
    assert "factors" in data
    assert "disclaimer" in data

def test_get_safety_score_invalid_coordinates(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="safety_bad_coords@example.com")
    response = client.get("/api/v1/safety-score?latitude=999.0&longitude=-122.4194", headers=headers)
    assert response.status_code == 422
