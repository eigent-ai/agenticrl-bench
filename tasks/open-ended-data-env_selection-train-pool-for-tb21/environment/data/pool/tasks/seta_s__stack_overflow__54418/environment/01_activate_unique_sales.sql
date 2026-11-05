UPDATE sales SET status = 'INACTIVE';

UPDATE sales SET status = 'ACTIVE'
WHERE id IN (
    SELECT DISTINCT (saleprice, saledate), id FROM sales HAVING count = 1
);
