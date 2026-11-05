-- Keep lowest tag_id for each tag_name, delete duplicates
DELETE `a` FROM `tags` AS `a`
INNER JOIN `tags` AS `b` USING `tag_name`
WHERE a.tag_id > b.tag_id;
