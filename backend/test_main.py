import pytest
from fastapi.testclient import TestClient
from main import app

# Create a mock client to send requests to your FastAPI app
client = TestClient(app)


def test_health_check():
    """Test 1: Does the health check return a 200 OK and unified format?"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_evaluation_endpoint():
    """Test 2: Does the evaluation endpoint return your candidate details?"""
    response = client.get("/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "candidateName" in data
    assert "features" in data


def test_login_success():
    """Test 3: Does the login route generate a JWT token for the admin?"""
    response = client.post(
        "/api/auth/login", data={"username": "singhshubham", "password": "singh123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure():
    """Test 4: Does the login route reject bad passwords?"""
    response = client.post(
        "/api/auth/login", data={"username": "singhshubham", "password": "wrong123"}
    )
    # Our global HTTP handler formats this as a 400 error
    assert response.status_code == 400


def test_protected_route_without_token():
    """Test 5: Does the API block unauthenticated users from creating meetings?"""
    response = client.post(
        "/api/meetings",
        json={
            "title": "Secret Meeting",
            "participants": ["test@test.com"],
            "meetingDate": "2026-05-20T10:00:00Z",
            "transcript": [],
        },
    )
    # Should return 401 Unauthorized because we didn't attach the JWT token
    assert response.status_code == 401
