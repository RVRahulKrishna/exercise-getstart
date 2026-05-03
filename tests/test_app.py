import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed, using in-memory data)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act: Sign up
    signup_response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: Signup
    assert signup_response.status_code == 200
    assert f"Signed up {email}" in signup_response.json()["message"]

    # Act: Remove
    delete_response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert: Remove
    assert delete_response.status_code == 200
    assert f"Removed {email}" in delete_response.json()["message"]

def test_signup_duplicate_participant():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already present in default data

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
