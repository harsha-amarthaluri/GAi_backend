def test_create_sos_incident_success(client, auth_headers_factory):
    headers, user = auth_headers_factory(email="sos_user@example.com")
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "trigger_type": "MANUAL"
    }
    response = client.post("/api/v1/sos", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user["id"]
    assert data["trigger_type"] == "MANUAL"
    assert data["status"] == "ALERTING"
    assert "id" in data

def test_create_sos_invalid_trigger_type(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="bad_sos_trigger@example.com")
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "trigger_type": "INVALID_TRIGGER"
    }
    response = client.post("/api/v1/sos", json=payload, headers=headers)
    assert response.status_code == 422

def test_sos_history_user_isolation(client, auth_headers_factory):
    headers_a, user_a = auth_headers_factory(email="sosa@example.com")
    headers_b, user_b = auth_headers_factory(email="sosb@example.com")

    # User A creates 2 SOS incidents
    client.post("/api/v1/sos", json={"latitude": 10.0, "longitude": 20.0, "trigger_type": "MANUAL"}, headers=headers_a)
    client.post("/api/v1/sos", json={"latitude": 11.0, "longitude": 21.0, "trigger_type": "SHAKE"}, headers=headers_a)

    # User B lists SOS incidents
    res_b = client.get("/api/v1/sos", headers=headers_b)
    assert res_b.status_code == 200
    data_b = res_b.json()
    assert data_b["total"] == 0
    assert len(data_b["items"]) == 0

    # User A lists SOS incidents
    res_a = client.get("/api/v1/sos", headers=headers_a)
    assert res_a.status_code == 200
    data_a = res_a.json()
    assert data_a["total"] == 2
    assert len(data_a["items"]) == 2

def test_sos_history_pagination(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="sos_page@example.com")
    for i in range(5):
        client.post("/api/v1/sos", json={"latitude": 10.0 + i, "longitude": 20.0 + i, "trigger_type": "MANUAL"}, headers=headers)

    res = client.get("/api/v1/sos?skip=0&limit=2", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["skip"] == 0
    assert data["limit"] == 2
