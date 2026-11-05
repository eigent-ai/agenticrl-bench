SELECT e.employee_id, e.first_name, e.last_name, e.department
FROM employees e
INNER JOIN active_badges b ON e.employee_id = b.employee_id
WHERE b.badge_id IS NULL;
