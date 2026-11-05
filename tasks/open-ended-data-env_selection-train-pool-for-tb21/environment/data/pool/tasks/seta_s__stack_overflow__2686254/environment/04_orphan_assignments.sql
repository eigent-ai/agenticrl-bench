SELECT da.id, da.employee_id, da.department, da.assigned_date
FROM department_assignments da
WHERE da.employee_id NOT IN (
  SELECT employee_id FROM employees
);
