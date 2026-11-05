SELECT e.id, e.name, c.path_length AS depth
FROM closure c
JOIN employees e ON e.id = c.ancestor_id
WHERE c.ancestor_id = ?
ORDER BY c.path_length, e.sort_order;
