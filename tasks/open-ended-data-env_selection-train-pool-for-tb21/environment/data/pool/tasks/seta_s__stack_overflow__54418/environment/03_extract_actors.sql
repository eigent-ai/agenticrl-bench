CREATE OR REPLACE VIEW all_actors AS
SELECT saved_by AS username FROM products
UNION ALL
SELECT deleted_by AS username FROM products
UNION ALL
SELECT accepted_by AS username FROM products
UNION ALL
SELECT published_by AS username FROM products;
