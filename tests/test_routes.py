from wsgiref import headers
import pytest
from app import create_app
from app.extensions import db
from config import TestingConfig

# -----------------------------
# Fixtures
# -----------------------------

# use fixtures from tests/conftest.py (app, client, auth_token)

# -----------------------------
# Tests
# -----------------------------

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"KasiLink API is running" in res.data

def get_auth_headers(client):
    # Register
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password"
    })
    # Login
    # Try login by email first, then username
    login_res = client.post("/auth/login", json={"email": "test@example.com", "password": "password"})
    if login_res.status_code != 200:
        login_res = client.post("/auth/login", json={"username": "testuser", "password": "password"})

    data = login_res.get_json()
    if not data or "access_token" not in data:
        raise AssertionError(f"login failed: status={login_res.status_code} body={login_res.get_data(as_text=True)}")

    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}  

def test_register_and_login(client):
    # Register new user
    res = client.post("/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass"
    })
    assert res.status_code == 201

    # Login new user
    res = client.post("/auth/login", json={
        "username": "newuser",
        "password": "newpass"
    })
    data = res.get_json()
    assert res.status_code == 200
    assert "access_token" in data

def test_create_post(client):
    # First register or login user
    client.post("/auth/register", json={
        "username": "tester",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    token = login_response.get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Then create post
    res = client.post("/posts/", json={
        "title": "Test Post",
        "content": "Test content"
    }, headers=headers)

    assert res.status_code == 201


def test_update_post(client, auth_headers):
    headers = auth_headers
    # Create first
    create_res = client.post("/posts/", json={
        "title": "Update Test",
        "content": "Before update"
    }, headers=headers)
    
    post_id = create_res.get_json()["id"]

    # Then update
    update_res = client.put(f"/posts/{post_id}", json={
        "title": "Updated Title"
    }, headers=headers)

    assert update_res.status_code == 200


def test_delete_post(client, auth_headers):
    headers = auth_headers
    # Create first
    create_res = client.post("/posts/", json={
        "title": "Delete Test",
        "content": "Test content"
    }, headers=headers)

    post_id = create_res.get_json()["id"]

    # Then delete
    del_res = client.delete(f"/posts/{post_id}", headers=headers)
    assert del_res.status_code == 200


def test_nearby_search(client, auth_headers):
    headers = auth_headers

    # Create two posts with coordinates: one near (lat=1.0, lon=1.0), one far (lat=10.0, lon=10.0)
    near = client.post("/posts/", json={
        "title": "Near Post",
        "content": "Nearby",
        "latitude": 1.0,
        "longitude": 1.0
    }, headers=headers)
    assert near.status_code == 201

    far = client.post("/posts/", json={
        "title": "Far Post",
        "content": "Far away",
        "latitude": 10.0,
        "longitude": 10.0
    }, headers=headers)
    assert far.status_code == 201

    # Query nearby around (1.0,1.0) with small radius
    res = client.get('/posts/nearby?lat=1.0&lon=1.0&radius_km=50')
    assert res.status_code == 200
    data = res.get_json()
    # Expect at least one result and the near post to be present
    titles = [p['title'] for p in data]
    assert 'Near Post' in titles
    assert 'Far Post' not in titles
