# Étape 1: Choisir l'image de base Python
FROM python:3.9-slim

# Étape 2: Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3: Copier le fichier requirements.txt
COPY requirements.txt /app/

# Étape 4: Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier tout le code dans le conteneur
COPY . /app/

# Étape 6: Exposer le port utilisé par l'application (ici 8000)
EXPOSE 8000

# Suppression des fichiers indésirables
RUN rm -rf /app/venv
RUN rm -rf /app/__pycache__


# Étape 7: Lancer l'application FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

