import pytest
from httpx import AsyncClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./client.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = db
    with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="module")
async def token(client):
    response = await client.post(
        "/token",
        data={"username": "user", "password": "password"}
    )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_client(client, token):
    response = await client.post(
        "/clients/",
        json={"name": "test_client", "email": "test_client@example.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test_client"
    assert response.json()["email"] == "test_client@example.com"

@pytest.mark.asyncio
async def test_read_clients(client, token):
    response = await client.get("/clients/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_client(client, token):
    response = await client.post(
        "/clients/",
        json={"name": "update_test", "email": "update_test@example.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    client_id = response.json()["id"]
    response = await client.put(
        f"/clients/{client_id}",
        json={"name": "updated_client", "email": "updated_client@example.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "updated_client"
    assert response.json()["email"] == "updated_client@example.com"

@pytest.mark.asyncio
async def test_delete_client(client, token):
    response = await client.post(
        "/clients/",
        json={"name": "delete_test", "email": "delete_test@example.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    client_id = response.json()["id"]
    response = await client.delete(
        f"/clients/{client_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Client deleted"}
