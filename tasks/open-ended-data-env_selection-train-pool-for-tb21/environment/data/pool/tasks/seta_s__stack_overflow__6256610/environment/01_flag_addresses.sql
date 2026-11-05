-- Update address flag columns based on presence in reference tables.

UPDATE address_records a
INNER JOIN customers_ref c
    ON (a.addr1 = c.addr1 AND a.city = c.city AND a.state = c.state AND a.zip = c.zip)
INNER JOIN suppliers_ref s
    ON (a.addr1 = s.addr1 AND a.city = s.city AND a.state = s.state AND a.zip = s.zip)
INNER JOIN partners_ref p
    ON (a.addr1 = p.addr1 AND a.city = p.city AND a.state = p.state AND a.zip = p.zip)
SET
    a.is_customer = CASE WHEN c.addr1 IS NOT NULL THEN TRUE ELSE FALSE END,
    a.is_supplier = CASE WHEN s.addr1 IS NOT NULL THEN TRUE ELSE FALSE END,
    a.is_partner  = CASE WHEN p.addr1 IS NOT NULL THEN TRUE ELSE FALSE END;
