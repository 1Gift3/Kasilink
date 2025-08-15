import pytest
from app import create_app, db
from app.models import User

pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test module."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def test_user(app):
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def auth_token(client, test_user):
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    return response.json['access_token']

