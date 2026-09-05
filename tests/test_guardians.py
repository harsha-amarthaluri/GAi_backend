def test_guardian_crud_success(client, auth_headers_factory):
    headers, user = auth_headers_factory(email="guardian_owner@example.com")
    
    # 1. Create Guardian
    create_payload = {
        "name": "Mom",
        "phone": "+123456789",
        "relationship": "Mother",
        "notification_enabled": True
    }
    create_res = client.post("/api/v1/guardians", json=create_payload, headers=headers)
    assert create_res.status_code == 201
    guardian = create_res.json()
    guardian_id = guardian["id"]
    assert guardian["name"] == "Mom"
    assert guardian["relationship"] == "Mother"

    # 2. List Guardians
    list_res = client.get("/api/v1/guardians", headers=headers)
    assert list_res.status_code == 200
    guardians = list_res.json()
    assert len(guardians) == 1
    assert guardians[0]["id"] == guardian_id

    # 3. Get Guardian
    get_res = client.get(f"/api/v1/guardians/{guardian_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == guardian_id

    # 4. Update Guardian
    update_payload = {"name": "Mom Updated", "phone": "+987654321"}
    update_res = client.put(f"/api/v1/guardians/{guardian_id}", json=update_payload, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Mom Updated"

    # 5. Delete Guardian
    del_res = client.delete(f"/api/v1/guardians/{guardian_id}", headers=headers)
    assert del_res.status_code == 204

    # Verify deleted
    get_after_del = client.get(f"/api/v1/guardians/{guardian_id}", headers=headers)
    assert get_after_del.status_code == 404

def test_user_cannot_access_another_users_guardian(client, auth_headers_factory):
    headers_user_a, user_a = auth_headers_factory(email="usera@example.com")
    headers_user_b, user_b = auth_headers_factory(email="userb@example.com")

    # User A creates a guardian
    create_res = client.post(
        "/api/v1/guardians",
        json={"name": "User A Guardian", "phone": "+100000", "relationship": "Friend"},
        headers=headers_user_a
    )
    guardian_id = create_res.json()["id"]

    # User B tries to GET User A's guardian
    get_res = client.get(f"/api/v1/guardians/{guardian_id}", headers=headers_user_b)
    assert get_res.status_code == 404

    # User B tries to PUT User A's guardian
    put_res = client.put(
        f"/api/v1/guardians/{guardian_id}",
        json={"name": "Hacked Name"},
        headers=headers_user_b
    )
    assert put_res.status_code == 404

    # User B tries to DELETE User A's guardian
    del_res = client.delete(f"/api/v1/guardians/{guardian_id}", headers=headers_user_b)
    assert del_res.status_code == 404
