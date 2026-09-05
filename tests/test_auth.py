def test_user_registration_success(client):
    payload = {
        "full_name": "Alice Smith",
        "email": "alice@example.com",
        "phone_number": "+1112223333",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["full_name"] == "Alice Smith"
    assert "hashed_password" not in data
    assert "password" not in data

def test_user_registration_duplicate_email(client):
    payload = {
        "full_name": "Bob Jones",
        "email": "bob@example.com",
        "password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=payload)
    # Attempt second registration with same email
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_success(client):
    register_payload = {
        "full_name": "Charlie Brown",
        "email": "charlie@example.com",
        "password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=register_payload)

    login_payload = {
        "email": "charlie@example.com",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    register_payload = {
        "full_name": "David Miller",
        "email": "david@example.com",
        "password": "CorrectPassword123!"
    }
    client.post("/api/v1/auth/register", json=register_payload)

    login_payload = {
        "email": "david@example.com",
        "password": "WrongPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401

def test_protected_endpoint_without_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403 or response.status_code == 401

def test_current_user_endpoint_success(client, auth_headers_factory):
    headers, user_data = auth_headers_factory(email="me@example.com")
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["id"] == user_data["id"]
