-- Seed data for appdb migration

INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Engineering', 'Software engineering department');
INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Marketing', 'Marketing and communications');
INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Finance', 'Financial operations');
INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Human Resources', 'HR and talent management');
INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Sales', 'Sales and business development');
INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Operations', 'Business operations');
INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Legal', 'Legal and compliance');
INSERT INTO departments (id, name, description) VALUES (dept_seq.NEXTVAL, 'Support', 'Customer support');

INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Alice', 'Johnson', 'alice@example.com', 1);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Bob', 'Smith', 'bob@example.com', 1);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Carol', 'Davis', 'carol@example.com', 2);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Dave', 'Wilson', 'dave@example.com', 3);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Eve', 'Brown', 'eve@example.com', 4);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Frank', 'Taylor', 'frank@example.com', 1);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Grace', 'Anderson', 'grace@example.com', 5);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Hank', 'Thomas', 'hank@example.com', 2);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Ivy', 'Jackson', 'ivy@example.com', 6);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Jack', 'White', 'jack@example.com', 7);
INSERT INTO employees (id, first_name, last_name, email, department_id) VALUES (emp_seq.NEXTVAL, 'Karen', 'Harris', 'karen@example.com', 8);
INSERT INTO employees (id, first_name, last_name, email, department_id, hire_date) VALUES (emp_seq.NEXTVAL, 'Leo', 'Martin', 'leo@example.com', 3, SYSDATE);

INSERT INTO projects (id, title, department_id, status) VALUES (proj_seq.NEXTVAL, 'Website Redesign', 1, 'active');
INSERT INTO projects (id, title, department_id, status) VALUES (proj_seq.NEXTVAL, 'Q4 Campaign', 2, 'active');
INSERT INTO projects (id, title, department_id, status) VALUES (proj_seq.NEXTVAL, 'Budget Review', 3, 'active');
INSERT INTO projects (id, title, department_id, status) VALUES (proj_seq.NEXTVAL, 'Hiring Drive', 4, 'active');
INSERT INTO projects (id, title, department_id, status) VALUES (proj_seq.NEXTVAL, 'Sales Dashboard', 5, 'active');

INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Design homepage mockup', 1, 1, 1, 'pending');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Implement login page', 2, 1, 2, 'pending');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Write marketing copy', 3, 2, 3, 'in_progress');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Review financial report', 4, 3, 1, 'pending');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Screen resumes', 5, 4, 2, 'pending');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Build API endpoints', 6, 1, 1, 'in_progress');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Create social media ads', 8, 2, 4, 'pending');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Audit expense reports', 4, 3, 2, 'pending');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Update CRM records', 7, 5, 3, 'pending');
INSERT INTO work_queue (workid, task_description, assigned_to, project_id, priority, status) VALUES ((SELECT wq_seq.NEXTVAL FROM dual), 'Draft contract template', 10, 5, 5, 'pending');
