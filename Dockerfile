# Utilisation d'une image Python officielle de base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . .

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer le port sur lequel l'application FastAPI s'exécute
EXPOSE 8000

# Commande pour démarrer l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
