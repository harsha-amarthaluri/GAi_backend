from fastapi.testclient import TestClient

def test_chat_message_endpoint_normal(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/chat/message",
        headers=auth_headers,
        json={"message": "How does Emergency SOS work?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["is_emergency_detected"] is False

def test_chat_message_endpoint_emergency_detected(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/chat/message",
        headers=auth_headers,
        json={"message": "Help me I am in danger and being followed!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_emergency_detected"] is True
    assert "TRIGGER_EMERGENCY_SOS" in data["suggested_actions"]
