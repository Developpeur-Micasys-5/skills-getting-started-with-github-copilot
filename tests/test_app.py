from src.app import activities


def test_root_redirect_to_static_index(client):
    # Arrange / Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 302)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    # Arrange / Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert set(["Chess Club", "Programming Class", "Gym Class"]).issubset(data.keys())

    for activity_name in ["Chess Club", "Programming Class", "Gym Class"]:
        assert "description" in data[activity_name]
        assert "schedule" in data[activity_name]
        assert "max_participants" in data[activity_name]
        assert "participants" in data[activity_name]
        assert isinstance(data[activity_name]["participants"], list)


def test_signup_success_adds_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    before_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert len(activities[activity_name]["participants"]) == before_count + 1
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange / Act
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "nobody@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_does_not_modify_other_activities(client):
    # Arrange
    target_activity = "Chess Club"
    other_activity = "Gym Class"
    email = "isolated.student@mergington.edu"
    other_before = list(activities[other_activity]["participants"])

    # Act
    response = client.post(f"/activities/{target_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert activities[other_activity]["participants"] == other_before
