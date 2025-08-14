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

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def auth_token(client):
    # Register user with email
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    })

    # Login
    login_resp = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    data = login_resp.get_json()
    return data["access_token"]

@pytest.fixture(autouse=True)
def clean_db():
    yield
    db.session.rollback()
