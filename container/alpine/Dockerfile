# Utilise l'image de base PostgreSQL avec Alpine Linux version 3.19
FROM alpine:3.19.1

# Supprime récursivement le répertoire de données PostgreSQL existant
RUN apk add py3-flask
RUN apk add py3-requests
RUN apk add py3-psycopg2
RUN apk add git

RUN git clone https://github.com/DevCloudSM/api_users.git
WORKDIR /api_users/app/

CMD python3 app.py
