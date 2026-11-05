SELECT
    p.name AS project_name,
    p.description AS project_description,
    a.notes AS assessment_notes,
    (SELECT GROUP_CONCAT(asr.name, ', ')
     FROM assessors asr
     WHERE asr.assessment_id = a.id) AS assessor_names
FROM projects p
JOIN assessments a ON a.project_id = p.id
ORDER BY p.name, a.id;
