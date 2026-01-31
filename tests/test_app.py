import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Reset activities to initial state before each test
@pytest.fixture(autouse=True)
def reset_activities():
    # Store initial state
    initial_activities = {
        "Basketball Team": {
            "description": "Join the school basketball team and compete in local leagues",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Practice soccer skills and play friendly matches",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu", "amelia@mergington.edu"]
        },
        "Drama Society": {
            "description": "Participate in theater productions and acting workshops",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["charlotte@mergington.edu", "jack@mergington.edu"]
        },
        "Mathletes": {
            "description": "Compete in math competitions and solve challenging problems",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["benjamin@mergington.edu", "ella@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["henry@mergington.edu", "grace@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    activities.clear()
    activities.update(initial_activities)
    yield

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "participants" in data["Basketball Team"]
    assert len(data["Basketball Team"]["participants"]) == 2

def test_signup_success():
    response = client.post("/activities/Basketball%20Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Basketball Team"]["participants"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Basketball%20Team/signup?email=test@mergington.edu")
    # Second signup
    response = client.post("/activities/Basketball%20Team/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Basketball%20Team/signup?email=test@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Basketball%20Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" not in data["Basketball Team"]["participants"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Basketball%20Team/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]