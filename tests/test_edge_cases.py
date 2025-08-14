import pytest
from flask_jwt_extended import create_access_token
from app.models import User

def test_register_existing_user(client):
    # Attempt duplicate registration
    res = client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    })
    assert res.status_code == 400

def test_login_wrong_password(client):
    res = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpass"
    })
    data = res.get_json()
    assert res.status_code == 401
    assert "Invalid credentials" in data["error"]

def test_access_with_invalid_jwt(client):
    res = client.get("/posts/protected", headers={
        "Authorization": "Bearer invalidtoken"
    })
    assert res.status_code == 404

def test_access_without_token(client):
    res = client.get("/posts/protected")
    assert res.status_code == 404

def test_create_post_unauthenticated(client):
    res = client.post("/posts/", json={
        "title": "Fail Post",
        "content": "No token"
    })
    assert res.status_code == 404

def test_create_post_missing_fields(client, auth_token):
    res = client.post("/posts/", json={
        "title": "Missing content"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 400

def test_create_post_invalid_data_type(client, auth_token):
    res = client.post("/posts/", json={
        "title": 123,  # should be string
        "content": True
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 400
