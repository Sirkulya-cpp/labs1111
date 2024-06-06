CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS links (
    id SERIAL PRIMARY KEY,
    long_url VARCHAR(255) NOT NULL,
    short_url VARCHAR(255) NOT NULL
);

-- Додайте інші команди для створення таблиць або інші дії за необхідності