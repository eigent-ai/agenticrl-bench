SELECT DISTINCT * FROM employees
INNER JOIN departments ON employees.Position = departments.Position
ORDER BY employees.PersonId;
