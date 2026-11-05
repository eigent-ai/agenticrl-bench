-- Calculate inventory restock alerts and projected costs from supplier data
UPDATE inventory_alerts SET
    restock_flag = CASE WHEN i.quantity < i.reorder_point THEN 'YES' ELSE 'NO' END,
    projected_cost = CASE WHEN i.quantity < i.reorder_point THEN (i.reorder_point - i.quantity) * s.unit_cost ELSE NULL END,
    supplier_status = 'active'
FROM inventory i
LEFT JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE s.region IS NOT NULL
  AND inventory_alerts.item_id = i.item_id;
