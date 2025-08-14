import pytest

def test_register_existing_user(client):
    # Attempt to register the same user twice
    client.post('/auth/register', json={
        "username": "edgeuser",
        "email": "edgeuser@example.com",
        "password": "edgepass"
    })
    res = client.post('/auth/register', json={
        "username": "edgeuser",
        "email": "edgeuser@example.com",
        "password": "edgepass"
    })
    assert res.status_code == 400
    assert "Username already exists" in res.get_json().get("error", "")

def test_login_wrong_password(client):
    client.post('/auth/register', json={
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "correctpass"
    })
    res = client.post('/auth/login', json={
        "username": "wrongpassuser",
        "password": "wrongpass"
    })
    assert res.status_code == 401
    assert "Invalid credentials" in res.get_json().get("error", "")

@pytest.mark.parametrize("username,password", [
    ("nonexistent", "anypass"),      # Wrong username
    ("testuser", "wrongpass")        # Wrong password
])
def test_login_invalid_credentials(client, username, password):
    """Login should fail with invalid username or password."""
    res = client.post('/auth/login', json={
        "username": username,
        "password": password
    })
    assert res.status_code == 401
    data = res.get_json()
    assert "Invalid credentials" in data.get("error", "")


def test_register_duplicate_user(client):
    """Registering an existing username should return 400."""
    client.post('/auth/register', json={
        "username": "duplicateuser",
        "email": "dup@example.com",
        "password": "pass123"
    })
    res = client.post('/auth/register', json={
        "username": "duplicateuser",
        "email": "dup2@example.com",
        "password": "pass123"
    })
    assert res.status_code == 400
    data = res.get_json()
    assert "Username already exists" in data.get("error", "")


def test_create_post_missing_fields(client, auth_token):
    # Missing title
    res = client.post('/posts/', json={
        "content": "Missing title",
        "category": "job",
        "location": "Zone 6"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 400
    assert "title" in res.get_json()["errors"]

def test_update_nonexistent_post(client, auth_token):
    res = client.put('/posts/9999', json={
        "title": "Should Fail"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 404
    assert "Post not found" in res.get_json()["error"]

def test_delete_nonexistent_post(client, auth_token):
    res = client.delete('/posts/9999',
                        headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 404
    assert "Post not found" in res.get_json()["error"]

def test_create_post_unauthenticated(client):
    res = client.post('/posts/', json={
        "title": "No Auth",
        "content": "Should fail",
        "category": "job",
        "location": "Zone 6"
    })
    assert res.status_code == 401
    assert "Missing Authorization" in res.get_json().get("msg", "")
