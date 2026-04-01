def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "malek",
        "email": "malek@test.com",
        "password": "test123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "account created successfully"
    assert data["user"]["email"] == "malek@test.com"
    assert "password" not in data["user"]


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "username": "malek",
        "email": "malek@test.com",
        "password": "test123"
    })
    response = client.post("/auth/register", json={
        "username": "malek2",
        "email": "malek@test.com",
        "password": "test123"
    })
    assert response.status_code == 409
    assert "email" in response.get_json()["error"]


def test_register_missing_fields(client):
    response = client.post("/auth/register", json={
        "email": "malek@test.com"
    })
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "username": "malek",
        "email": "malek@test.com",
        "password": "test123"
    })
    response = client.post("/auth/login", json={
        "email": "malek@test.com",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert data["token"] is not None


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "malek",
        "email": "malek@test.com",
        "password": "test123"
    })
    response = client.post("/auth/login", json={
        "email": "malek@test.com",
        "password": "mauvais_mot_de_passe"
    })
    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post("/auth/login", json={
        "email": "inconnu@test.com",
        "password": "test123"
    })
    assert response.status_code == 401