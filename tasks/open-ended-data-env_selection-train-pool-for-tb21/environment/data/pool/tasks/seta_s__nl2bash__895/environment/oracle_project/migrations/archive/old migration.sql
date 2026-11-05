-- Legacy migration script
-- Original author: J. Smith
-- Date: 2017-11-03
-- Used in production Oracle 11g environment
SELECT pending_count FROM dba_2pc_pending WHERE rownum < 10;

-- The above query was used for monitoring
-- Replaced by newer procedures in 2019
