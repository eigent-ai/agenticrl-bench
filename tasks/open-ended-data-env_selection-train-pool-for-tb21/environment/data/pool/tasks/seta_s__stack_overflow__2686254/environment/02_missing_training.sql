SELECT r.first_name, r.last_name, r.course_name
FROM required_training r
LEFT JOIN training_completions t
  ON r.first_name <> t.first_name
  AND r.last_name <> t.last_name
  AND r.course_name <> t.course_name
WHERE t.id IS NULL;
