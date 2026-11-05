ATTACH DATABASE 'sources/eng.db' AS eng_src;

INSERT INTO students SELECT student_id, student_name, email, department, credits FROM eng_src.students;
INSERT INTO enrollments SELECT enrollment_id, student_id, course_code, semester FROM eng_src.enrollments;

DETACH DATABASE eng_src;
