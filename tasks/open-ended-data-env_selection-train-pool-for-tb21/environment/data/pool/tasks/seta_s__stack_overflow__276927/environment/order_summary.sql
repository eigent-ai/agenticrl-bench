SELECT
    o.order_id,
    o.customer_name,
    o.order_date,
    o.status,
    oi.product_name,
    oi.quantity,
    oi.unit_price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
ORDER BY o.order_id;
