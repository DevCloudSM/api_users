-- Crée la base de données user_db
CREATE DATABASE user_db;

-- Sélectionne la base de données user_db
\c user_db;

-- Crée la table des utilisateurs s'ils n'existent pas déjà
CREATE TABLE IF NOT EXISTS users (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL
);

-- Insère des données initiales dans la table des utilisateurs
INSERT INTO users (name, surname, username, email) VALUES
    ('Doe', 'John', 'John_Doe', 'john@example.com'),
    ('Smith', 'Jane', 'Jane_Smith', 'jane@example.com');
