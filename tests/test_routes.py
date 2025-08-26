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

def test_create_post(client, auth_headers):
    res = client.post("/posts/posts", json={
        "title": "Test Post",
        "content": "Test content"
    }, headers=auth_headers)
    
    assert res.status_code == 201


def test_update_post(client, auth_headers):
    # Create first
    create_res = client.post("/posts/posts", json={
        "title": "Update Test",
        "content": "Before update"
    }, headers=auth_headers)
    
    post_id = create_res.get_json()["id"]

    # Then update
    update_res = client.put(f"/posts/{post_id}", json={
        "title": "Updated Title"
    }, headers=auth_headers)

    assert update_res.status_code == 200


def test_delete_post(client, auth_headers):
    # Create first
    create_res = client.post("/posts/posts", json={
        "title": "Delete Test",
        "content": "Test content"
    }, headers=auth_headers)
    
    post_id = create_res.get_json()["id"]

    # Then delete
    del_res = client.delete(f"/posts/{post_id}", headers=auth_headers)
    assert del_res.status_code == 200
