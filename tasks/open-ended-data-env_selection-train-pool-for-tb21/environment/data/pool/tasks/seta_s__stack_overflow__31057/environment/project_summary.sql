SELECT
    p.name AS project_name,
    a.notes AS assessment_notes
FROM projects p
JOIN assessments a ON a.project_id = p.id
ORDER BY p.name, a.id;
