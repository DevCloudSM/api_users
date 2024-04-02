# Utilise l'image de base PostgreSQL avec Alpine Linux version 3.19
FROM postgres:alpine3.19

# Supprime récursivement le répertoire de données PostgreSQL existant
RUN rm -rf /var/lib/postgresql/data

# Copie le fichier init.sql depuis le système hôte vers le répertoire
# utilisé par PostgreSQL pour l'initialisation de la base de données
COPY ./init.sql /docker-entrypoint-initdb.d/
