import pytest
from app import create_app, db

@pytest.fixture(scope="function")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def auth_headers(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "test123"
    })
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "test123"
    })
    token = response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}