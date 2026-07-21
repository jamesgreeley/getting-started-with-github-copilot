from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


BASE_ACTIVITIES = deepcopy(activities)


import pytest


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(deepcopy(BASE_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(BASE_ACTIVITIES))


def test_get_activities_returns_seed_data():
    # Arrange
    expected_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club",
    }

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert set(payload) == expected_names
    assert payload["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_rejects_duplicate_participant():
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_updates_activity():
    # Arrange
    email = "michael@mergington.edu"
    before = activities["Chess Club"]["participants"][:]

    # Act
    response = client.delete(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert email not in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == len(before) - 1
