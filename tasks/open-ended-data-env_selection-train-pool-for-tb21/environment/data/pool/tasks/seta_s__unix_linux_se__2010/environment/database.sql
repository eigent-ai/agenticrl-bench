CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token VARCHAR(128) NOT NULL,
    expires_at TIMESTAMP NOT NULL
);

INSERT INTO users (username, email) VALUES
    ('admin', 'admin@example.com'),
    ('deploy', 'deploy@example.com');
