-- Delete posts whose project no longer exists
DELETE FROM posts
LEFT JOIN projects ON projects.project_id = posts.project_id
WHERE projects.project_id IS NULL;
