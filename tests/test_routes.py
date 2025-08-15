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
        "email": "newuser@example.com",
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
    res = client.get("/")
    assert res.status_code == 200
    assert b"KasiLink API is running" in res.data

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

def test_create_post(client, auth_token):
    res = client.post("/posts/", json={
        "title": "Test Post",
        "content": "Test content",
        "category": "job",
        "location": "Zone 1"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 201

def test_update_post(client, auth_token):
    # First create post
    create_res = client.post("/posts/", json={
        "title": "Update Test",
        "content": "Before update"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    post_id = create_res.json['id']
    
    # Then update it
    update_res = client.put(f"/posts/{post_id}", json={
        "title": "Updated Title"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert update_res.status_code == 200

def test_delete_post(client, auth_token):
    # First create post
    create_res = client.post("/posts/", json={
        "title": "Delete Test",
        "content": "Test content"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    post_id = create_res.json['id']
    
    # Then delete it
    del_res = client.delete(f"/posts/{post_id}",
                          headers={"Authorization": f"Bearer {auth_token}"})
    assert del_res.status_code == 200