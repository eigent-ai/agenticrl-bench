CREATE TABLE dba_tables (
    owner TEXT NOT NULL,
    table_name TEXT NOT NULL,
    tablespace_name TEXT,
    status TEXT DEFAULT 'VALID'
);

CREATE TABLE dba_objects (
    owner TEXT NOT NULL,
    object_name TEXT NOT NULL,
    object_type TEXT NOT NULL,
    status TEXT DEFAULT 'VALID'
);

CREATE TABLE user_tab_cols (
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    column_id INTEGER NOT NULL,
    data_type TEXT NOT NULL
);

-- SYS tables
INSERT INTO dba_tables VALUES ('SYS', 'DUAL', 'SYSTEM', 'VALID');
INSERT INTO dba_tables VALUES ('SYS', 'TAB$', 'SYSTEM', 'VALID');
INSERT INTO dba_tables VALUES ('SYS', 'OBJ$', 'SYSTEM', 'VALID');
INSERT INTO dba_tables VALUES ('SYS', 'COL$', 'SYSTEM', 'VALID');
INSERT INTO dba_tables VALUES ('SYS', 'USER$', 'SYSTEM', 'VALID');
INSERT INTO dba_tables VALUES ('SYS', 'SEG$', 'SYSTEM', 'VALID');
INSERT INTO dba_tables VALUES ('SYS', 'TS$', 'SYSTEM', 'VALID');
INSERT INTO dba_tables VALUES ('SYS', 'IND$', 'SYSTEM', 'VALID');

-- HR tables
INSERT INTO dba_tables VALUES ('HR', 'EMPLOYEES', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('HR', 'DEPARTMENTS', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('HR', 'JOBS', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('HR', 'LOCATIONS', 'USERS', 'VALID');

-- SALES tables (real)
INSERT INTO dba_tables VALUES ('SALES', 'CUSTOMERS', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('SALES', 'ORDERS', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('SALES', 'ORDER_ITEMS', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('SALES', 'PRODUCTS', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('SALES', 'REGIONS', 'USERS', 'VALID');

-- SALES recyclebin entries
INSERT INTO dba_tables VALUES ('SALES', 'BIN$aE7tQ==', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('SALES', 'BIN$rR3kW==', 'USERS', 'VALID');
INSERT INTO dba_tables VALUES ('SALES', 'BIN$zZ9pL==', 'USERS', 'VALID');

-- dba_objects (matching entries)
INSERT INTO dba_objects VALUES ('SYS', 'DUAL', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SYS', 'TAB$', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SYS', 'OBJ$', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SYS', 'COL$', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SYS', 'USER$', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SYS', 'SEG$', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SYS', 'TS$', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SYS', 'IND$', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('HR', 'EMPLOYEES', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('HR', 'DEPARTMENTS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('HR', 'JOBS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('HR', 'LOCATIONS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'CUSTOMERS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'ORDERS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'ORDER_ITEMS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'PRODUCTS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'REGIONS', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'BIN$aE7tQ==', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'BIN$rR3kW==', 'TABLE', 'VALID');
INSERT INTO dba_objects VALUES ('SALES', 'BIN$zZ9pL==', 'TABLE', 'VALID');

-- user_tab_cols: SYS tables
INSERT INTO user_tab_cols VALUES ('DUAL', 'DUMMY', 1, 'VARCHAR2');

INSERT INTO user_tab_cols VALUES ('TAB$', 'OBJ#', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('TAB$', 'DATAOBJ#', 2, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('TAB$', 'TS#', 3, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('OBJ$', 'OBJ#', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('OBJ$', 'DATAOBJ#', 2, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('OBJ$', 'OWNER#', 3, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('OBJ$', 'NAME', 4, 'VARCHAR2');

INSERT INTO user_tab_cols VALUES ('COL$', 'OBJ#', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('COL$', 'COL#', 2, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('COL$', 'NAME', 3, 'VARCHAR2');

INSERT INTO user_tab_cols VALUES ('USER$', 'USER#', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('USER$', 'NAME', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('USER$', 'PASSWORD', 3, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('USER$', 'DATATS#', 4, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('SEG$', 'FILE#', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('SEG$', 'BLOCK#', 2, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('SEG$', 'TS#', 3, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('TS$', 'TS#', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('TS$', 'NAME', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('TS$', 'BLOCKSIZE', 3, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('IND$', 'OBJ#', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('IND$', 'DATAOBJ#', 2, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('IND$', 'TS#', 3, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('IND$', 'BO#', 4, 'NUMBER');

-- user_tab_cols: HR tables
INSERT INTO user_tab_cols VALUES ('EMPLOYEES', 'EMPLOYEE_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('EMPLOYEES', 'FIRST_NAME', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('EMPLOYEES', 'LAST_NAME', 3, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('EMPLOYEES', 'EMAIL', 4, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('EMPLOYEES', 'HIRE_DATE', 5, 'DATE');
INSERT INTO user_tab_cols VALUES ('EMPLOYEES', 'SALARY', 6, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('DEPARTMENTS', 'DEPARTMENT_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('DEPARTMENTS', 'DEPARTMENT_NAME', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('DEPARTMENTS', 'MANAGER_ID', 3, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('DEPARTMENTS', 'LOCATION_ID', 4, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('JOBS', 'JOB_ID', 1, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('JOBS', 'JOB_TITLE', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('JOBS', 'MIN_SALARY', 3, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('JOBS', 'MAX_SALARY', 4, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('LOCATIONS', 'LOCATION_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('LOCATIONS', 'STREET_ADDRESS', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('LOCATIONS', 'CITY', 3, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('LOCATIONS', 'COUNTRY_ID', 4, 'VARCHAR2');

-- user_tab_cols: SALES tables
INSERT INTO user_tab_cols VALUES ('CUSTOMERS', 'CUSTOMER_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('CUSTOMERS', 'CUSTOMER_NAME', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('CUSTOMERS', 'EMAIL', 3, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('CUSTOMERS', 'REGION_ID', 4, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('ORDERS', 'ORDER_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('ORDERS', 'CUSTOMER_ID', 2, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('ORDERS', 'ORDER_DATE', 3, 'DATE');
INSERT INTO user_tab_cols VALUES ('ORDERS', 'TOTAL_AMOUNT', 4, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('ORDERS', 'STATUS', 5, 'VARCHAR2');

INSERT INTO user_tab_cols VALUES ('ORDER_ITEMS', 'ORDER_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('ORDER_ITEMS', 'ITEM_ID', 2, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('ORDER_ITEMS', 'PRODUCT_ID', 3, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('ORDER_ITEMS', 'QUANTITY', 4, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('ORDER_ITEMS', 'UNIT_PRICE', 5, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('PRODUCTS', 'PRODUCT_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('PRODUCTS', 'PRODUCT_NAME', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('PRODUCTS', 'CATEGORY', 3, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('PRODUCTS', 'PRICE', 4, 'NUMBER');

INSERT INTO user_tab_cols VALUES ('REGIONS', 'REGION_ID', 1, 'NUMBER');
INSERT INTO user_tab_cols VALUES ('REGIONS', 'REGION_NAME', 2, 'VARCHAR2');
INSERT INTO user_tab_cols VALUES ('REGIONS', 'COUNTRY', 3, 'VARCHAR2');
