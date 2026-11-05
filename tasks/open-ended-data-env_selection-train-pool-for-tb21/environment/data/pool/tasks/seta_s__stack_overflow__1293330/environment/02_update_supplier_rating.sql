UPDATE p
SET p.supplier_rating = s.rating
FROM product p
INNER JOIN supplier s ON p.supplier_id = s.id;
