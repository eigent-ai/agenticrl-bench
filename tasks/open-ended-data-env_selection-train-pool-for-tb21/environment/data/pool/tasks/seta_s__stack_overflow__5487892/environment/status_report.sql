SELECT t.id AS turbine_id, t.name, t.status, t.rpm,
    CASE status
        WHEN 'active' THEN 'Running'
        WHEN rpm > 500 THEN 'High Speed'
        ELSE 'Other'
    END AS status_category
FROM turbines t
ORDER BY t.id;
