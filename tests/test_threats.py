def test_create_and_get_threats(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="threat_user@example.com")
    
    # 1. Create threat
    payload = {
        "category": "CRIME",
        "severity": 8.0,
        "title": "Robbery Reported",
        "description": "Armed robbery near main station",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "radius": 1000.0,
        "source": "POLICE",
        "confidence": 0.95,
        "is_active": True
    }
    create_res = client.post("/api/v1/threats", json=payload, headers=headers)
    assert create_res.status_code == 201
    data = create_res.json()
    assert data["title"] == "Robbery Reported"
    assert data["category"] == "CRIME"
    assert data["severity"] == 8.0

    # 2. Get threats near coordinates
    get_res = client.get("/api/v1/threats?latitude=37.7749&longitude=-122.4194&radius=2000", headers=headers)
    assert get_res.status_code == 200
    list_data = get_res.json()
    assert list_data["total"] >= 1
    assert any(t["title"] == "Robbery Reported" for t in list_data["items"])

def test_get_threats_category_filter(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="filter_user@example.com")

    # Query with category filter
    res = client.get("/api/v1/threats?category=CRIME", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
