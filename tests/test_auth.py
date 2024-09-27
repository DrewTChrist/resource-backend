from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_auth_route():
    data = None
    response = client.post(
        "/api/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "admin", "password": "admin"},
    )
    json = response.json()
    assert "access_token" in json
    assert "token_type" in json
