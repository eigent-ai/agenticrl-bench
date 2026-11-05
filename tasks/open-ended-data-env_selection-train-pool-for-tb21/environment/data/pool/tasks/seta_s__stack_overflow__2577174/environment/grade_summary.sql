USE school_mgmt;

CREATE OR REPLACE VIEW grade_summary AS
SELECT
    u.username,
    u.given_name,
    u.family_name,
    c.course_name,
    g.assignment,
    g.score,
    g.graded_date
FROM users u
INNER JOIN classes_users cu ON u.username = cu.username AND cu.role = 'student'
INNER JOIN classes c ON cu.classes_id = c.id
INNER JOIN grades g ON g.username = u.username AND g.classes_id = c.id;
