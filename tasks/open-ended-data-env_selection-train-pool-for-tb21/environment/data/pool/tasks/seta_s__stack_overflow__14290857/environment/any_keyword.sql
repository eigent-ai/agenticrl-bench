SELECT id, title, description, category, content
FROM documents
WHERE content LIKE '%{any_keywords_0}%'
  AND content LIKE '%{any_keywords_1}%';
