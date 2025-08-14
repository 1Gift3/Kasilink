import pytest
from app import create_app
from app.extensions import db 
from config import TestingConfig 

@pytest.fixture(scope='module')
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

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
    # ignore if user exists
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
