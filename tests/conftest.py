import pytest
from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    """Flask test client for making requests."""
    return app.test_client()

@pytest.fixture(scope="module")
def test_user(app):
    """Create a test user in the database."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.password = "testpass"  # uses the setter to hash
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post('/auth/login', json={
        "username": test_user.username,
        "password": "testpass"
    })
    assert response.status_code == 200, response.get_data(as_text=True)

    token = response.get_json()["access_token"]
    # JWT Authorization header must be in this format:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers(auth_token):
    """Return headers containing JWT token for authorized requests."""
    return {"Authorization": f"Bearer {auth_token}"}
