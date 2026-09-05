def test_sos_incident_audit_trail_events(client, auth_headers):
    # 1. Trigger SOS Incident
    sos_payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "trigger_type": "MANUAL"
    }
    sos_res = client.post("/api/v1/sos", json=sos_payload, headers=auth_headers)
    assert sos_res.status_code == 201
    sos_data = sos_res.json()
    sos_id = sos_data["id"]

    # 2. Fetch Audit Events for created SOS
    events_res = client.get(f"/api/v1/sos/{sos_id}/events", headers=auth_headers)
    assert events_res.status_code == 200
    events = events_res.json()

    assert len(events) >= 3
    event_types = [e["event_type"] for e in events]
    assert "SOS_CREATED" in event_types
    assert "LOCATION_CAPTURED" in event_types
    assert "GUARDIAN_NOTIFICATION_SENT" in event_types
