UPDATE location_codes
SET code = REPLACE(code, '01', '09')
WHERE code LIKE '% 01';
