-- Resolve old string IDs to integer user_id for created_by and last_updated_by.

UPDATE users u
SET created_by = sub.user_id
FROM users sub
WHERE u.created_by_old = sub.user_old_id;
