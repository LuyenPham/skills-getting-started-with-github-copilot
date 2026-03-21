import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange & Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_valid():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Cleanup
    client.delete(f"/activities/{activity}/signup", params={"email": email})

def test_signup_already_signed_up():
    activity = "Chess Club"
    email = "michael@mergington.edu"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_valid():
    activity = "Programming Class"
    email = "tempuser@mergington.edu"
    # Sign up first
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

def test_unregister_not_found():
    activity = "Programming Class"
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
