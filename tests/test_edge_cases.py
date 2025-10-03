import pytest
from flask_jwt_extended import create_access_token
from app.models import User

def test_register_existing_user(client, test_user):
    res = client.post("/auth/register", json={
        "username": "testuser",  # Duplicate username
        "email": "new@example.com",
        "password": "password123"
    })
    assert res.status_code == 400
    assert b"already exists" in res.data

def test_login_wrong_password(client, test_user):
    res = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert res.status_code == 401
    assert b"Invalid credentials" in res.data

def test_access_with_invalid_jwt(client):
    res = client.get("/posts/protected", headers={
        "Authorization": "Bearer invalidtoken"
    })
    assert res.status_code == 401  # Changed from 404

def test_access_without_token(client):
    res = client.get("/posts/protected")
    assert res.status_code == 401  # Changed from 404

def test_create_post_unauthenticated(client):
    res = client.post("/posts/posts", json={
        "title": "Fail Post",
        "content": "No token"
    })
    assert res.status_code == 401 

def test_create_post(client, auth_token):
    response = client.post(
        '/posts/posts',
        json={
            'title': 'Test Post',
            'content': 'Test content',
            'category': 'job',
            'location': 'Zone 1'
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201

    

def test_create_post_invalid_data_type(client, auth_token):
    res = client.post("/posts/posts", json={
        "title": 123,  # should be string
        "content": True
    }, headers={"Authorization": f"Bearer {auth_token}"})
    # API coerces title/content to strings and creates the post
    assert res.status_code == 201
