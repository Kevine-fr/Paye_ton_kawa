from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, engine

# Créez les tables dans la base de données
Base.metadata.create_all(bind=engine)

print("Tables créées avec succès")
