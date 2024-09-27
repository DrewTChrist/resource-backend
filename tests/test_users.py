from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def authenticate(username: str, password: str) -> str:
    response = client.post(
        "/api/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "password": password},
    )
    return response.json()["access_token"]


def test_get_current_user():
    access_token = authenticate("admin", "admin")
    response = client.get(
        "/api/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    json = response.json()
    assert json == {
        "user_id": 1,
        "first_name": "admin",
        "last_name": "admin",
        "username": "admin",
        "disabled": False,
        "admin": True,
    }
