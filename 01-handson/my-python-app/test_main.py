import uuid

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_create_user(client: TestClient):
    email = f"alice-{uuid.uuid4().hex[:8]}@example.com"
    response = client.post("/users/", json={"name": "Alice", "email": email})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == email
    assert "id" in data

def test_read_users(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)