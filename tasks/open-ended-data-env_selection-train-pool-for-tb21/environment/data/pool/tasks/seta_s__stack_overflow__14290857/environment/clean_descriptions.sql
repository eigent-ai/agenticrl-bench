SELECT id, title, description, category
FROM documents
WHERE description LIKE '%{word_target}%';
