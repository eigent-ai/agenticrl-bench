SELECT table_name, LISTAGG(column_name, ',') WITHIN GROUP (ORDER BY column_id) AS columns FROM user_tab_cols GROUP BY table_name ORDER BY table_name;
