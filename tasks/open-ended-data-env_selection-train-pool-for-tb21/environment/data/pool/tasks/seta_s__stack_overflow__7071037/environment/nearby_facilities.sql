SELECT
  facility_id, facility_name, facility_lat, facility_lng,
  ROUND(3956 * 2 * ASIN(SQRT(POWER(SIN((39.97780609 - ABS(facility_lat)) * PI() / 180 / 2), 2) + COS(39.97780609 * PI() / 180) * COS(ABS(facility_lat) * PI() / 180) * POWER(SIN((-105.25861359 - facility_lng) * PI() / 180 / 2), 2))), 2) AS distance
FROM facilities
HAVING distance <= 0.50 AND distance > 0.00
ORDER BY distance;
