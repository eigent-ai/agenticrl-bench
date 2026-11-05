SELECT name FROM catalog_online
UNION ALL
SELECT name FROM catalog_retail
ORDER BY name;
