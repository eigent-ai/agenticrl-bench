SELECT e.id, e.name,
    (SELECT COUNT(*) FROM closure ct2 WHERE ct2.ancestor_id = e.id AND ct2.path_length > 0) AS depth
FROM closure c
JOIN employees e ON e.id = c.ancestor_id
WHERE c.descendant_id = ?;
