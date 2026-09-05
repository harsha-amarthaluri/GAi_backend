def test_delete_user_account(client, auth_headers_factory):
    headers, _ = auth_headers_factory(email="delete_me@example.com")
    
    # 1. Delete profile
    res = client.delete("/api/v1/users/me", headers=headers)
    assert res.status_code == 204

    # 2. Verify subsequent requests fail with 401
    get_res = client.get("/api/v1/users/me", headers=headers)
    assert get_res.status_code in [401, 404]
