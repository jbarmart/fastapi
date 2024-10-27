# test_main.py
import pytest
from unittest.mock import patch

from prometheus_client import REGISTRY

from app.config import settings
from app.tests.conftest import Base, engine, TestingSessionLocal


@pytest.fixture(scope="function", autouse=True)
def setup_function():
    # Clear data before each test
    db = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db.close()

def test_get_user(client, statcode=404):
    headers = {"token": "test-token"}
    response = client.get("/get_user/1", headers=headers)
    assert response.status_code == statcode


def test_get_user_after_create(client):
    # First, create a user
    payload = {"user_id": 1, "username": "jacob"}
    headers = {"token": "test-token"}
    create = client.post("/create_user", json=payload, headers=headers)
    create.status_code == 201

    test_get_user(client, statcode=200)


def test_update_user(client):
    # First, create a user
    payload = {"user_id": 1, "username": "jacob"}
    update_payload = { "user_id": 1, "username": "update_jacob"}
    headers = {"token": "test-token"}

    create = client.post("/create_user", json=payload, headers=headers)
    assert create.status_code == 200

    # Update the user's information
    update = client.put(f"/update_user?user_id={update_payload['user_id']}", json=update_payload, headers=headers)
    assert update.status_code == 200

    # Verify the update
    response = client.get("/get_user/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "update_jacob"

def test_update_user_long(client):

    update_payload = { "user_id": 1, "username": "update_jacob"}
    headers = {"token": "test-token"}

    test_get_user(client, statcode=404)
    test_get_user_after_create(client)

    update = client.put(f"/update_user?user_id={update_payload['user_id']}", json=update_payload, headers=headers)
    assert update.status_code == 200

    test_get_user(client, statcode=200)


def test_health_check(client):
    response = client.get("/health", headers={"token": "test-token"})
    assert response.status_code == 200
    assert response.json() == settings.VALUE


def test_metrics(client):
    # Make a request to trigger the metrics
    response = client.get("/health", headers={"token": "test-token"})
    assert response.status_code == 200
    client.get("/health", headers={"token": "test-token"})
    client.get("/health", headers={"token": "test-token"})

    # Fetch the metrics
    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    metrics_data = metrics_response.text

    # Assert the metric value
    assert 'http_requests_total{handler="/health",method="GET",status="2xx"} 3.0' in metrics_data
