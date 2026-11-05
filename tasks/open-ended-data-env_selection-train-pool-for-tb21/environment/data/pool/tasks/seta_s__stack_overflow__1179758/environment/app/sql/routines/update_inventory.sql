CREATE OR REPLACE PROCEDURE update_inventory()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT oi.product_id, SUM(oi.quantity) AS total_qty
        FROM order_items oi
        JOIN orders o ON o.id = oi.order_id
        WHERE o.status = 'processed'
        GROUP BY oi.product_id
    LOOP
        UPDATE inventory SET quantity = quantity - r.total_qty
        WHERE product_id = r.product_id;
    END LOOP;
END;
$$;
