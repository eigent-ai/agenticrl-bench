COPY (SELECT * FROM revenue_summary ORDER BY category) TO 'output/revenue_summary.csv' WITH CSV HEADER DELIMITER ',';
