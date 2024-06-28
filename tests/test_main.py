import pytest
from fastapi.testclient import TestClient
from main import app, create_access_token
from datetime import datetime, timedelta

client = TestClient(app)

# Simulating token generation for testing purposes
@pytest.fixture(scope="module")
def access_token():
    return create_access_token(data={"sub": "user"})

# Test endpoint for login and obtaining access token
def test_login():
    # Attempt to log in with valid credentials
    response = client.post("/token", params={"username": "user", "password": "password"})

    assert response.status_code == 200
    assert "access_token" in response.json()


# Test CRUD operations for clients
def test_create_client(access_token):
    response = client.post("/clients/",
                           headers={"Authorization": f"Bearer {access_token}"},
                           json={"name": "John Doe", "email": "john.doe@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john.doe@example.com"

def test_read_clients(access_token):
    response = client.get("/clients/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_client(access_token):
    # Create a client first
    response_create = client.post("/clients/",
                                  headers={"Authorization": f"Bearer {access_token}"},
                                  json={"name": "Jane Smith", "email": "jane.smith@example.com"})
    client_id = response_create.json()["id"]

    # Retrieve the created client
    response_read = client.get(f"/clients/{client_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response_read.status_code == 200
    assert response_read.json()["name"] == "Jane Smith"
    assert response_read.json()["email"] == "jane.smith@example.com"


# Test update_client and delete_client functionalities
def test_update_client(access_token):
    # Create a client first
    response_create = client.post("/clients/",
                                  headers={"Authorization": f"Bearer {access_token}"},
                                  json={"name": "Update Test Client", "email": "update.test@example.com"})
    client_id = response_create.json()["id"]

    # Prepare updated data
    updated_data = {
        "name": "Updated Client Name",
        "email": "updated.client@example.com"
    }

    # Attempt to update the client
    response_update = client.put(f"/clients/{client_id}",
                                 headers={"Authorization": f"Bearer {access_token}"},
                                 json=updated_data)
    assert response_update.status_code == 200

    # Verify the updated client details
    response_get_updated = client.get(f"/clients/{client_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response_get_updated.status_code == 200
    assert response_get_updated.json()["name"] == "Updated Client Name"
    assert response_get_updated.json()["email"] == "updated.client@example.com"

def test_delete_client(access_token):
    # Create a client first
    response_create = client.post("/clients/",
                                  headers={"Authorization": f"Bearer {access_token}"},
                                  json={"name": "Delete Test Client", "email": "delete.test@example.com"})
    client_id = response_create.json()["id"]

    # Attempt to delete the client
    response_delete = client.delete(f"/clients/{client_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response_delete.status_code == 200

    # Verify the deletion message
    assert response_delete.json()["message"] == "Client deleted"

    # Attempt to fetch the deleted client to verify it's not found
    response_get_deleted = client.get(f"/clients/{client_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response_get_deleted.status_code == 404


