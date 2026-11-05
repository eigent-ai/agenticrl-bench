SELECT customer_id, name, email FROM customers
UNION
SELECT order_id, product, amount FROM orders;
