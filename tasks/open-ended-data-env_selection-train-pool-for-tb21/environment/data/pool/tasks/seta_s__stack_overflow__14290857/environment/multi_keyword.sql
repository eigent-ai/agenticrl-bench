SELECT id, title, description, category, content
FROM documents
WHERE content LIKE '%{multi_keywords_0}%'
   OR content LIKE '%{multi_keywords_1}%'
   OR content LIKE '%{multi_keywords_2}%';
