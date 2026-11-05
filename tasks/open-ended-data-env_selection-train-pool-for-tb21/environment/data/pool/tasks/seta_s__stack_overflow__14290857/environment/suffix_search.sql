SELECT id, title, category
FROM documents
WHERE category LIKE '%{suffix_target}%';
