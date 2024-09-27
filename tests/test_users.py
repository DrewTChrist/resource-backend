"""Tests for user related routes

Three users are added for testing. See sql/test_data.sql.

usernames: admin, disabled, user
password: admin
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def authenticate(username: str, password: str) -> str:
    """Return an access token for use with tests"""
    response = client.post(
        "/api/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "password": password},
    )
    return response.json()["access_token"]


def test_get_users():
    """Test the route for fetching all users

    Any administrator should be able to access this route.
    """
    access_token = authenticate("admin", "admin")
    response = client.get(
        "/api/users/", headers={"Authorization": f"Bearer {access_token}"}
    )
    json = response.json()
    assert len(json) == 3
    assert json[0] == {
        "user_id": 1,
        "first_name": "admin",
        "last_name": "admin",
        "username": "admin",
        "disabled": False,
        "admin": True,
    }


def test_get_users_failure():
    """Test the route for fetching all users

    This test expects a failure from the endpoint. Regular users
    will receive an error.
    """
    access_token = authenticate("user", "admin")
    response = client.get(
        "/api/users/", headers={"Authorization": f"Bearer {access_token}"}
    )
    json = response.json()
    assert response.status_code == 403
    assert json == {"detail": "Insufficient permissions"}


def test_get_current_user():
    """Test route for fetching current user"""
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


def test_get_current_user_failure():
    """Test route for fetching current user

    This test expects a failure from the endpoint. There is no access token
    sent in the request so no user is authenticated.
    """
    response = client.get("/api/users/me")
    json = response.json()
    assert response.status_code == 401
    assert json == {"detail": "Not authenticated"}
