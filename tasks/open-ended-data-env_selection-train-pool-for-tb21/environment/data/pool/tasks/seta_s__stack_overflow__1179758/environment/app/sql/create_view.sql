CREATE OR REPLACE VIEW order_summary AS
SELECT
    o.id AS order_id,
    o.customer_name,
    get_order_total(o.id) AS total,
    o.discount,
    o.status
FROM orders o
WHERE get_order_total(o.id) > 0;
