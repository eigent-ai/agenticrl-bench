DROP TABLE IF EXISTS contacts_deduped;

SELECT DISTINCT ON (name), id, metadata
INTO contacts_deduped
FROM contacts
ORDER BY name, id;
