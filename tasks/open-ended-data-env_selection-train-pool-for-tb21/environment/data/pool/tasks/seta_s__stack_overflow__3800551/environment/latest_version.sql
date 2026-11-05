SELECT server_id, version, installed_at
FROM (
    SELECT server_id, version, installed_at,
           ROW_NUMBER() OVER (PARTITION BY server_id ORDER BY MAX(version) DESC) as rn
    FROM software_versions
    GROUP BY server_id, version, installed_at
) sub
WHERE rn = 1
ORDER BY server_id;
