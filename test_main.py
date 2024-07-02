import sys
import os
import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import uuid  # Pour générer des UUID uniques
from sqlalchemy.orm import declarative_base

# Ajouter le répertoire parent au PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

SQLALCHEMY_DATABASE_URL = "sqlite:///./client.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Fixture for the database
@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Override the get_db dependency to use the testing session
@pytest_asyncio.fixture(scope="module")
async def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test", transport=ASGITransport(app=app)) as ac:
        yield ac

@pytest_asyncio.fixture(scope="module")
async def token(client):
    response = await client.post(
        "/token",
        data={"username": "user", "password": "password"}
    )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_client(client, token):
    unique_name = f"test_client_{uuid.uuid4().hex}"  # Utilisation d'un UUID unique
    try:
        response = await client.post(
            "/clients/",
            json={"name": unique_name, "email": f"{unique_name}@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == unique_name
        assert response.json()["email"] == f"{unique_name}@example.com"
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during client creation: {e.orig}")

@pytest.mark.asyncio
async def test_read_clients(client, token):
    response = await client.get("/clients/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_client_by_id(client, token):
    unique_name = f"test_client_by_id_{uuid.uuid4().hex}"  # Utilisation d'un UUID unique
    try:
        # Create a client first
        create_response = await client.post(
            "/clients/",
            json={"name": unique_name, "email": f"{unique_name}@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert create_response.status_code == 201

        client_id = create_response.json()["id"]

        # Get the client by ID
        read_response = await client.get(
            f"/clients/{client_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert read_response.status_code == 200
        assert read_response.json()["name"] == unique_name
        assert read_response.json()["email"] == f"{unique_name}@example.com"
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during client read by ID: {e.orig}")

@pytest.mark.asyncio
async def test_update_client(client, token):
    unique_name = f"update_test_{uuid.uuid4().hex}"  # Utilisation d'un UUID unique
    try:
        # Create a client first
        create_response = await client.post(
            "/clients/",
            json={"name": unique_name, "email": f"{unique_name}@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert create_response.status_code == 201

        client_id = create_response.json()["id"]

        # Update the client
        update_response = await client.put(
            f"/clients/{client_id}",
            json={"name": f"updated_{unique_name}", "email": f"updated_{unique_name}@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == f"updated_{unique_name}"
        assert update_response.json()["email"] == f"updated_{unique_name}@example.com"
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during client update: {e.orig}")

@pytest.mark.asyncio
async def test_delete_client(client, token):
    try:
        # Create a client first
        create_response = await client.post(
            "/clients/",
            json={"name": "delete_test", "email": "delete_test@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert create_response.status_code == 201

        client_id = create_response.json()["id"]

        # Delete the client
        delete_response = await client.delete(
            f"/clients/{client_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert delete_response.status_code == 200
        assert delete_response.json() == {"message": "Client deleted"}
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during client deletion: {e.orig}")
