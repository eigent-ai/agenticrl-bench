SELECT TOP 5 id, name, email, region
FROM participants
WHERE region = '{REGION}'
ORDER BY RAND();
