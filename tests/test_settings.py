from fastapi.testclient import TestClient

def test_user_settings_get_and_update(client: TestClient, auth_headers: dict):
    # 1. Get settings
    get_resp = client.get(
        "/api/v1/users/settings",
        headers=auth_headers
    )
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["shake_sos_enabled"] is True

    # 2. Update settings
    update_resp = client.put(
        "/api/v1/users/settings",
        headers=auth_headers,
        json={"shake_sos_enabled": False, "voice_distress_enabled": True}
    )
    assert update_resp.status_code == 200
    updated_data = update_resp.json()
    assert updated_data["shake_sos_enabled"] is False
    assert updated_data["voice_distress_enabled"] is True
