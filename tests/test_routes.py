import pytest
from app import create_app
from app.extensions import db
from config import TestingConfig

# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture(scope='module')
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def auth_token(client):
    # Register user
    register_resp = client.post('/auth/register', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    })
    # Ignore if user exists already (201 = created, 400 = user exists)
    if register_resp.status_code not in (201, 400):
        pytest.fail("Failed to register user")

    # Login user
    login_resp = client.post('/auth/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert login_resp.status_code == 200
    data = login_resp.get_json()
    assert "access_token" in data
    return data["access_token"]

# -----------------------------
# Tests
# -----------------------------

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"KasiLink API is running" in res.data

def test_register_and_login(client):
    # Register a new user to avoid conflicts
    res = client.post('/auth/register', json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass"
    })
    assert res.status_code == 201

    # Login
    login_res = client.post('/auth/login', json={
        "username": "newuser",
        "password": "newpass"
    })
    assert login_res.status_code == 200
    data = login_res.get_json()
    assert "access_token" in data

def test_create_post(client, auth_token):
    post_data = {
        "title": "Test Job",
        "content": "Need help with groceries",
        "category": "job",
        "location": "Zone 6"
    }
    res = client.post('/posts/', json=post_data,
                      headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Test Job"

def test_update_post(client, auth_token):
    # Create post first
    post_data = {
        "title": "Original Title",
        "content": "Original content",
        "category": "job",
        "location": "Zone 6"
    }
    create_res = client.post('/posts/', json=post_data,
                             headers={"Authorization": f"Bearer {auth_token}"})
    assert create_res.status_code == 201
    post_id = create_res.get_json()["id"]

    # Update the post
    update_data = {
        "title": "Updated Title",
        "content": "Updated content"
    }
    update_res = client.put(f'/posts/{post_id}', json=update_data,
                            headers={"Authorization": f"Bearer {auth_token}"})
    assert update_res.status_code == 200
    updated_post = update_res.get_json()
    assert updated_post["title"] == "Updated Title"
    assert updated_post["content"] == "Updated content"

def test_delete_post(client, auth_token):
    # Create post first
    post_data = {
        "title": "To be deleted",
        "content": "Delete me please",
        "category": "job",
        "location": "Zone 6"
    }
    res = client.post('/posts/', json=post_data,
                      headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 201
    post_id = res.get_json()["id"]

    # Delete the post
    del_res = client.delete(f'/posts/{post_id}',
                            headers={"Authorization": f"Bearer {auth_token}"})
    assert del_res.status_code == 200
    assert del_res.get_json()["msg"] == "Post deleted"
