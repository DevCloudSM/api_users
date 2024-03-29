CREATE DATABASE user_db;
\c user_db;
CREATE TABLE IF NOT EXISTS users (
    ID SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL, CONSTRAINT AK_username UNIQUE(username),
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

INSERT INTO users (username, name, surname, email) VALUES
('john_doe', 'John', 'Doe', 'john@example.com'),
('jane_smith', 'Jane', 'Smith', 'jane@example.com');

