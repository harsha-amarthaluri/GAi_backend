def test_get_user_profile(client, auth_headers_factory):
    headers, user_data = auth_headers_factory(email="profile@example.com", full_name="Original Name")
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Original Name"

def test_update_user_profile(client, auth_headers_factory):
    headers, user_data = auth_headers_factory(email="updateprofile@example.com")
    update_payload = {
        "full_name": "Updated Name",
        "phone_number": "+9998887777"
    }
    response = client.put("/api/v1/users/me", json=update_payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["phone_number"] == "+9998887777"
