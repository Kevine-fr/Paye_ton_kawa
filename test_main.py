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

SQLALCHEMY_DATABASE_URL = "sqlite:///./product.db"
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
async def product(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test", transport=ASGITransport(app=app)) as ac:
        yield ac

@pytest_asyncio.fixture(scope="module")
async def token(product):
    response = await product.post(
        "/token",
        data={"username": "user", "password": "password"}
    )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_product(product, token):
    unique_name = f"test_product_{uuid.uuid4().hex}"  # Utilisation d'un UUID unique
    try:
        response = await product.post(
            "/products/",
            json={
                "name": unique_name,
                "description": f"Description for {unique_name}",
                "image": "test_image.jpg",
                "price": 9.99,
                "qte": 100
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == unique_name
        assert response.json()["description"] == f"Description for {unique_name}"
        assert response.json()["image"] == "test_image.jpg"
        assert response.json()["price"] == 9.99
        assert response.json()["qte"] == 100
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during product creation: {e.orig}")

@pytest.mark.asyncio
async def test_read_products(product, token):
    response = await product.get("/products/" , headers={"Authorization": f"Bearer {token}"}
)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_product_by_id(product , token):
    unique_name = f"test_product_by_id_{uuid.uuid4().hex}"  # Utilisation d'un UUID unique
    try:
        # Create a product first
        create_response = await product.post(
            "/products/",
            json={
                "name": unique_name,
                "description": f"Description for {unique_name}",
                "image": "test_image.jpg",
                "price": 9.99,
                "qte": 100
            },            
            headers={"Authorization": f"Bearer {token}"}

        )
        assert create_response.status_code == 201

        product_id = create_response.json()["id"]

        # Get the product by ID
        read_response = await product.get(f"/products/{product_id}" , headers={"Authorization": f"Bearer {token}"})
        
        assert read_response.status_code == 200
        assert read_response.json()["name"] == unique_name
        assert read_response.json()["description"] == f"Description for {unique_name}"
        assert read_response.json()["image"] == "test_image.jpg"
        assert read_response.json()["price"] == 9.99
        assert read_response.json()["qte"] == 100
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during product read by ID: {e.orig}")

@pytest.mark.asyncio
async def test_update_product(product , token):
    unique_name = f"update_test_{uuid.uuid4().hex}"  # Utilisation d'un UUID unique
    try:
        # Create a product first
        create_response = await product.post(
            "/products/",
            json={
                "name": unique_name,
                "description": f"Description for {unique_name}",
                "image": "test_image.jpg",
                "price": 9.99,
                "qte": 100
            },            
            headers={"Authorization": f"Bearer {token}"}

        )
        assert create_response.status_code == 201

        product_id = create_response.json()["id"]

        # Update the product
        update_response = await product.put(
            f"/products/{product_id}",
            json={
                "name": f"updated_{unique_name}",
                "description": f"Updated description for {unique_name}",
                "image": "updated_image.jpg",
                "price": 19.99,
                "qte": 50
            },            
            headers={"Authorization": f"Bearer {token}"}
        )

        assert update_response.status_code == 200
        assert update_response.json()["name"] == f"updated_{unique_name}"
        assert update_response.json()["description"] == f"Updated description for {unique_name}"
        assert update_response.json()["image"] == "updated_image.jpg"
        assert update_response.json()["price"] == 19.99
        assert update_response.json()["qte"] == 50
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during product update: {e.orig}")

@pytest.mark.asyncio
async def test_delete_product(product , token):
    try:
        # Create a product first
        create_response = await product.post(
            "/products/",
            json={
                "name": "delete_test",
                "description": "Description for delete_test",
                "image": "test_image.jpg",
                "price": 9.99,
                "qte": 100
            },        
            headers={"Authorization": f"Bearer {token}"}

        )
        assert create_response.status_code == 201

        product_id = create_response.json()["id"]

        # Delete the product
        delete_response = await product.delete(f"/products/{product_id}" , headers={"Authorization": f"Bearer {token}"})

        assert delete_response.status_code == 200
        assert delete_response.json() == {"message": "Product deleted"}
    except IntegrityError as e:
        pytest.fail(f"Unexpected IntegrityError during product deletion: {e.orig}")

