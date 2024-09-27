from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_auth_route():
    response = client.post(
        "/api/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "admin", "password": "admin"},
    )
    json = response.json()
    assert "access_token" in json
    assert "token_type" in json


def test_auth_route_failure():
    response = client.post(
        "/api/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "admin", "password": "badpassword"},
    )
    json = response.json()
    assert response.status_code == 401
    assert json == {"detail": "Incorrect username or password"}
