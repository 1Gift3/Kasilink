import pytest
from app import create_app
from app.extensions import db

@pytest.fixture(scope='module')
def app():
    # Create app with test config
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key"
    })

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
    client.post('/auth/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    })
    # Login user
    login_response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    data = login_response.get_json()
    return data["access_token"]

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"KasiLink API is running" in res.data

def test_register_and_login(client):
    # Register a different user to avoid conflict with auth_token fixture
    res = client.post('/auth/register', json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass"
    })
    assert res.status_code == 201

    res = client.post('/auth/login', json={
        "username": "newuser",
        "password": "newpass"
    })
    assert res.status_code == 200
    data = res.get_json()
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
    
    print(res.get_json())

    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Test Job"

    
