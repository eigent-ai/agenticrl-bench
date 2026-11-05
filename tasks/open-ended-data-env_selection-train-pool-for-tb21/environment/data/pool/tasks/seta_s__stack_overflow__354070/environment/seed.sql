-- Customers
INSERT INTO Customers VALUES (1, 'Acme Corp', 'acme@example.com', 'New York');
INSERT INTO Customers VALUES (2, 'Globex Inc', 'globex@example.com', 'Chicago');
INSERT INTO Customers VALUES (3, 'Initech', 'initech@example.com', 'Austin');
INSERT INTO Customers VALUES (4, 'Umbrella Ltd', 'umbrella@example.com', 'Seattle');
INSERT INTO Customers VALUES (5, 'Stark Industries', 'stark@example.com', 'Boston');

-- Products
INSERT INTO Products VALUES (1, 'Widget-A', 'Widgets', 25.00);
INSERT INTO Products VALUES (2, 'Widget-B', 'Widgets', 35.00);
INSERT INTO Products VALUES (3, 'Gadget-X', 'Gadgets', 50.00);
INSERT INTO Products VALUES (4, 'Gadget-Y', 'Gadgets', 75.00);
INSERT INTO Products VALUES (5, 'Doohickey-1', 'Parts', 10.00);
INSERT INTO Products VALUES (6, 'Doohickey-2', 'Parts', 15.00);
INSERT INTO Products VALUES (7, 'Thingamajig', 'Parts', 20.00);
INSERT INTO Products VALUES (8, 'Whatchamacallit', 'Accessories', 45.00);

-- Suppliers
INSERT INTO Suppliers VALUES (1, 'SupplyCo', 'supply@example.com');
INSERT INTO Suppliers VALUES (2, 'PartsMaster', 'parts@example.com');
INSERT INTO Suppliers VALUES (3, 'GlobalParts', 'global@example.com');
INSERT INTO Suppliers VALUES (4, 'QuickShip', 'quick@example.com');
INSERT INTO Suppliers VALUES (5, 'MegaSupply', 'mega@example.com');

-- Orders (10 orders, 2 per customer)
INSERT INTO Orders VALUES (1, 1, '2025-01-15', 'confirmed');
INSERT INTO Orders VALUES (2, 1, '2025-02-10', 'confirmed');
INSERT INTO Orders VALUES (3, 2, '2025-01-20', 'confirmed');
INSERT INTO Orders VALUES (4, 2, '2025-02-15', 'processing');
INSERT INTO Orders VALUES (5, 3, '2025-01-25', 'confirmed');
INSERT INTO Orders VALUES (6, 3, '2025-03-01', 'pending');
INSERT INTO Orders VALUES (7, 4, '2025-02-20', 'confirmed');
INSERT INTO Orders VALUES (8, 4, '2025-01-10', 'cancelled');
INSERT INTO Orders VALUES (9, 5, '2025-03-05', 'processing');
INSERT INTO Orders VALUES (10, 5, '2025-01-30', 'confirmed');

-- OrderLines (2 per order = 20 lines)
INSERT INTO OrderLines VALUES (1, 1, 1, 5, 25.00);
INSERT INTO OrderLines VALUES (2, 1, 3, 2, 50.00);
INSERT INTO OrderLines VALUES (3, 2, 2, 3, 35.00);
INSERT INTO OrderLines VALUES (4, 2, 5, 10, 10.00);
INSERT INTO OrderLines VALUES (5, 3, 4, 1, 75.00);
INSERT INTO OrderLines VALUES (6, 3, 6, 4, 15.00);
INSERT INTO OrderLines VALUES (7, 4, 1, 8, 25.00);
INSERT INTO OrderLines VALUES (8, 4, 7, 3, 20.00);
INSERT INTO OrderLines VALUES (9, 5, 3, 6, 50.00);
INSERT INTO OrderLines VALUES (10, 5, 8, 2, 45.00);
INSERT INTO OrderLines VALUES (11, 6, 2, 5, 35.00);
INSERT INTO OrderLines VALUES (12, 6, 4, 1, 75.00);
INSERT INTO OrderLines VALUES (13, 7, 5, 15, 10.00);
INSERT INTO OrderLines VALUES (14, 7, 6, 7, 15.00);
INSERT INTO OrderLines VALUES (15, 8, 1, 2, 25.00);
INSERT INTO OrderLines VALUES (16, 8, 3, 1, 50.00);
INSERT INTO OrderLines VALUES (17, 9, 7, 4, 20.00);
INSERT INTO OrderLines VALUES (18, 9, 8, 3, 45.00);
INSERT INTO OrderLines VALUES (19, 10, 2, 6, 35.00);
INSERT INTO OrderLines VALUES (20, 10, 4, 2, 75.00);

-- Shipments (only for orders 1, 3, 5, 10 -- the rest are unshipped)
INSERT INTO Shipments VALUES (1, 1, '2025-01-20', 'FedEx');
INSERT INTO Shipments VALUES (2, 3, '2025-01-25', 'UPS');
INSERT INTO Shipments VALUES (3, 5, '2025-02-01', 'DHL');
INSERT INTO Shipments VALUES (4, 10, '2025-02-05', 'FedEx');

-- Returns (mix of before and after 2025-01-01)
INSERT INTO Returns VALUES (1, 9, 3, '2024-06-15', 'defective');
INSERT INTO Returns VALUES (2, 10, 8, '2024-11-20', 'wrong item');
INSERT INTO Returns VALUES (3, 1, 1, '2025-02-10', 'defective');
INSERT INTO Returns VALUES (4, 5, 4, '2025-01-15', 'not as described');
INSERT INTO Returns VALUES (5, 7, 1, '2025-03-01', 'damaged');
INSERT INTO Returns VALUES (6, 11, 2, '2025-02-20', 'wrong item');
INSERT INTO Returns VALUES (7, 13, 5, '2024-12-01', 'defective');
INSERT INTO Returns VALUES (8, 19, 2, '2025-01-25', 'not as described');

-- Inventory (some zero-stock entries; QuickShip and MegaSupply have issues)
INSERT INTO Inventory VALUES (1, 1, 1, 100, 'Warehouse-A');
INSERT INTO Inventory VALUES (2, 1, 2, 50, 'Warehouse-A');
INSERT INTO Inventory VALUES (3, 2, 3, 75, 'Warehouse-B');
INSERT INTO Inventory VALUES (4, 2, 5, 200, 'Warehouse-B');
INSERT INTO Inventory VALUES (5, 3, 4, 30, 'Warehouse-C');
INSERT INTO Inventory VALUES (6, 3, 7, 0, 'Warehouse-C');
INSERT INTO Inventory VALUES (7, 4, 6, 0, 'Warehouse-D');
INSERT INTO Inventory VALUES (8, 4, 8, 0, 'Warehouse-D');
