SELECT s.name AS supplier_name,
       s.contact_email,
       p.name AS product_name,
       i.quantity,
       i.warehouse
FROM Suppliers s
LEFT JOIN Inventory i ON s.SupplierID = i.supplier_id
    AND i.quantity > 0
LEFT JOIN Products p ON i.ProductID = p.ProductID;
