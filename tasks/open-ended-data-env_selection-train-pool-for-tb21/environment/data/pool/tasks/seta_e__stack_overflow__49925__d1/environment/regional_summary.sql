SELECT COUNT(*) AS count, 'east' AS region FROM transactions_east
UNION ALL
SELECT COUNT(*) AS count, 'west' AS region FROM transactions_west;
