SELECT o.OrderID,
       c.name AS customer_name,
       o.order_date,
       o.status
FROM Orders o
LEFT JOIN Shipments s ON o.OrderID = s.OrderID
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.status = 'confirmed'
  AND s.ShipmentID IS NULL;
