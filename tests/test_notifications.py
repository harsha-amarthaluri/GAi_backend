def test_register_fcm_token_success(client, auth_headers):
    payload = {
        "device_id": "android_device_test_123",
        "fcm_token": "fcm_token_sample_abc123xyz",
        "platform": "android"
    }
    response = client.post("/api/v1/notifications/token", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == "android_device_test_123"
    assert data["fcm_token"] == "fcm_token_sample_abc123xyz"
    assert data["is_active"] is True

def test_send_push_notification(client, auth_headers):
    # First register token
    token_payload = {
        "device_id": "android_device_test_123",
        "fcm_token": "fcm_token_sample_abc123xyz",
        "platform": "android"
    }
    client.post("/api/v1/notifications/token", json=token_payload, headers=auth_headers)

    # Send notification
    dispatch_payload = {
        "title": "🚨 EMERGENCY ALERT",
        "body": "Test push dispatch",
        "incident_id": "sample-incident-123"
    }
    response = client.post("/api/v1/notifications/send", json=dispatch_payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DISPATCH_SUCCESS"
    assert data["dispatched_count"] >= 1
