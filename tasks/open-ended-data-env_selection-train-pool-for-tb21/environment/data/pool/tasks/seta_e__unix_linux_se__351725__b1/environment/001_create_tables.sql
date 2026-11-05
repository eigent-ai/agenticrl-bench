CREATE TABLE IF NOT EXISTS releases (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL UNIQUE,
    deployed_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending'
);

INSERT INTO releases (version, status) VALUES ('1.0.0', 'deployed')
ON CONFLICT (version) DO UPDATE SET status = 'deployed';
