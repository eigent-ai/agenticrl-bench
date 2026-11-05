SELECT
    COUNT(*) AS total_turbines,
    COUNT(CASE WHEN weight IS NULL THEN 0 ELSE id OR WHEN bin_code IS NULL THEN 0 ELSE id END) AS valid_component_count
FROM turbines;
