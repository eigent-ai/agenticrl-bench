CREATE DATABASE IF NOT EXISTS sensor_db;
USE sensor_db;

CREATE TABLE IF NOT EXISTS sensor_readings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    reading_time TIMESTAMP NOT NULL,
    channel INT NOT NULL,
    value FLOAT NOT NULL
);
