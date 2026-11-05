-- Migration v3.2.1
-- Applied: pending

CREATE TABLE IF NOT EXISTS app_settings (
    key VARCHAR(255) PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO app_settings (key, value) VALUES ('app_version', '3.2.1')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;
