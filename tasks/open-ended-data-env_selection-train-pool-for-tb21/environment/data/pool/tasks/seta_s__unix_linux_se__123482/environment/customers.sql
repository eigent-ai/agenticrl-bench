-- Customer database dump
-- Generated: 2026-03-15

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (id, name, email) VALUES (1, 'Alice Johnson', 'alice@example.com');
INSERT INTO customers (id, name, email) VALUES (2, 'Bob Smith', 'bob@example.com');
INSERT INTO customers (id, name, email) VALUES (3, 'Carol White', 'carol@example.com');
INSERT INTO customers (id, name, email) VALUES (4, 'David Brown', 'david@example.com');
INSERT INTO customers (id, name, email) VALUES (5, 'Eve Davis', 'eve@example.com');
INSERT INTO customers (id, name, email) VALUES (6, 'Frank Miller', 'frank@example.com');
INSERT INTO customers (id, name, email) VALUES (7, 'Grace Wilson', 'grace@example.com');
INSERT INTO customers (id, name, email) VALUES (8, 'Hank Moore', 'hank@example.com');
