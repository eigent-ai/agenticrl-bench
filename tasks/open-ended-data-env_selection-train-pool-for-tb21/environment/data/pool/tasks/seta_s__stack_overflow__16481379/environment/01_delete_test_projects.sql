DELETE p FROM projects p INNER JOIN tasks t ON t.project_id = p.id WHERE p.title LIKE 'test%';
