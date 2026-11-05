-- Inventory database dump
-- Generated: 2026-03-15

CREATE TABLE inventory (
    id INTEGER PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) UNIQUE,
    stock_count INTEGER DEFAULT 0,
    warehouse VARCHAR(100)
);

INSERT INTO inventory (id, product_name, sku, stock_count, warehouse) VALUES (1, 'Widget A', 'WA-001', 150, 'Warehouse East');
INSERT INTO inventory (id, product_name, sku, stock_count, warehouse) VALUES (2, 'Widget B', 'WB-002', 75, 'Warehouse East');
INSERT INTO inventory (id, product_name, sku, stock_count, warehouse) VALUES (3, 'Widget C', 'WC-003', 200, 'Warehouse West');
INSERT INTO inventory (id, product_name, sku, stock_count, warehouse) VALUES (4, 'Gadget X', 'GX-010', 30, 'Warehouse East');
INSERT INTO inventory (id, product_name, sku, stock_count, warehouse) VALUES (5, 'Gadget Y', 'GY-011', 12, 'Warehouse West');
INSERT INTO inventory (id, product_name, sku, stock_count, warehouse) VALUES (6, 'Gadget Z', 'GZ-012', 0, 'Warehouse West');
