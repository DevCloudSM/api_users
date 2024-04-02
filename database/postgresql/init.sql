-- Crée la base de données user_db
CREATE DATABASE IF NOT EXISTS user_db;

-- Sélectionne la base de données user_db
\c user_db;

-- Crée la table des utilisateurs s'ils n'existent pas déjà
CREATE TABLE IF NOT EXISTS users (
    ID SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Insère des données initiales dans la table des utilisateurs
INSERT INTO users (username, name, surname, email) VALUES
    ('john_doe', 'John', 'Doe', 'john@example.com'),
    ('jane_smith', 'Jane', 'Smith', 'jane@example.com');
