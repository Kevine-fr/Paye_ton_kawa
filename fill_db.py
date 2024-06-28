# fill_db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import Client, SQLALCHEMY_DATABASE_URL  # Assurez-vous d'importer votre modèle Client et la configuration de votre base de données

# Configure SQLAlchemy to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Définition de quelques clients de test
test_clients = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Charlie", "email": "charlie@example.com"}
]

def fill_database():
    # Create all tables in the database (optional, only needed if tables don't exist yet)
    Base.metadata.create_all(bind=engine)

    # Create a session to interact with the database
    db = SessionLocal()

    try:
        # Insert test clients into the database
        for client_data in test_clients:
            db_client = Client(name=client_data["name"], email=client_data["email"])
            db.add(db_client)
        db.commit()
        print("Database filled with test data successfully!")
    except Exception as e:
        print(f"Failed to fill database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    fill_database()
