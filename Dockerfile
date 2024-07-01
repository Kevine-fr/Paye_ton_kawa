FROM python:3.9-slim

# Installer Node.js et npm
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    apt-get clean

WORKDIR /app

# Optionnel : Création de l'environnement virtuel (si nécessaire)
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copie des fichiers de l'application dans le répertoire de travail
COPY . .

# Installation des dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install pytest httpx

# Installation des dépendances Node.js (ajoutez package.json si nécessaire)
COPY package*.json ./
RUN npm install

# Exposer le port 8000 (si nécessaire)
EXPOSE 8000

# Commande par défaut pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
