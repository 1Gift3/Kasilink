import pytest
from app import create_app
from app.extensions import db
from app.models import User
from sqlalchemy.exc import IntegrityError

@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        # Ensure a test user exists in the database so different test_client
        # instances can authenticate against the same DB. This avoids issues
        # with sqlite in-memory databases and separate connections.
        from app.models import User
        if not User.query.filter_by(username='testuser').first():
            u = User(username='testuser', email='test@example.com')
            u.password = 'password'
            db.session.add(u)
            db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    """Flask test client for making requests."""
    return app.test_client()

@pytest.fixture(scope="module")
def test_user(app):
    """Create a test user in the database."""
    # Use the app's register endpoint via the test client to ensure consistent creation
    with app.app_context():
        with app.test_client() as c:
            resp = c.post('/auth/register', json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password'
            })
            # 201 = created, 400 = already exists
            if resp.status_code not in (201, 400):
                pytest.fail(f"Failed to ensure test user exists: {resp.status_code} {resp.get_data(as_text=True)}")

        return User.query.filter_by(username="testuser").first()
@pytest.fixture(scope="module")
def auth_token(client):
    """Return a JWT access token string for the test user, registering if necessary."""
    # Try to login first
    resp = client.post('/auth/login', json={"username": "testuser", "password": "password"})
    if resp.status_code != 200:
        # attempt to register then login
        reg = client.post('/auth/register', json={"username": "testuser", "email": "test@example.com", "password": "password"})
        assert reg.status_code in (200, 201, 400), f"Unexpected register response: {reg.status_code} {reg.get_data(as_text=True)}"

    assert resp.status_code == 200, resp.get_data(as_text=True)
    data = resp.get_json()
    assert "access_token" in data
    return data["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Return headers containing JWT token for authorized requests."""
    return {"Authorization": f"Bearer {auth_token}"}
