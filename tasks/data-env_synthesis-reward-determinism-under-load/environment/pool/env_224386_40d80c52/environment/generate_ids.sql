USE product_catalog;
SELECT id FROM expired_products WHERE expiry_date < '2025-01-01' ORDER BY id INTO OUTFILE '/tmp/ids_to_delete.txt' LINES TERMINATED BY '\n';
