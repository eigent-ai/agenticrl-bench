CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200),
    price DECIMAL(10,2),
    stock INT
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    path VARCHAR(500),
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE error_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(20),
    message TEXT,
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_trail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(100),
    table_name VARCHAR(100),
    record_id INT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE temp_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cache_key VARCHAR(200),
    cache_value TEXT,
    expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE session_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_token VARCHAR(256),
    user_id INT,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE USER IF NOT EXISTS 'backup_user'@'localhost' IDENTIFIED BY 'backup123';
GRANT SELECT, LOCK TABLES, SHOW VIEW, TRIGGER, EVENT ON appdb.* TO 'backup_user'@'localhost';
FLUSH PRIVILEGES;
