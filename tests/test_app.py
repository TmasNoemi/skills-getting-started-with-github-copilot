import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup?email=" + email)
    assert response.status_code == 200
    assert f"Signed up {email} for Chess Club" in response.json()["message"]


def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_for_activity_not_found():
    email = "someone@mergington.edu"
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_success():
    email = "daniel@mergington.edu"
    response = client.post(f"/activities/Chess Club/unregister", json={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email} from Chess Club" in response.json()["message"]


def test_unregister_participant_not_registered():
    email = "notregistered@mergington.edu"
    response = client.post(f"/activities/Chess Club/unregister", json={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not registered"


def test_unregister_activity_not_found():
    email = "someone@mergington.edu"
    response = client.post(f"/activities/Nonexistent/unregister", json={"email": email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
