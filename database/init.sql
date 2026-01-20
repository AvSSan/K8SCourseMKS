CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL
);

INSERT INTO books (title, author) VALUES ('Docker Entry Level', 'Unknown Author');
INSERT INTO books (title, author) VALUES ('Spring Boot Guide', 'Pivotal');