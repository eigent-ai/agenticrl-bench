-- Summary views for reporting dashboard
-- Author: Analytics Team

CREATE OR REPLACE VIEW v_daily_summary AS
SELECT TRUNC(txn_date) as report_date,
       COUNT(*) as total_transactions,
       SUM(CASE WHEN status = 'committed' THEN 1 ELSE 0 END) as committed_count,
       SUM(CASE WHEN status = 'rolled_back' THEN 1 ELSE 0 END) as rollback_count
FROM transaction_log
GROUP BY TRUNC(txn_date);

CREATE OR REPLACE VIEW v_weekly_trend AS
SELECT TRUNC(txn_date, 'IW') as week_start,
       COUNT(*) as weekly_total
FROM transaction_log
WHERE txn_date > SYSDATE - 90
GROUP BY TRUNC(txn_date, 'IW');

GRANT SELECT ON v_daily_summary TO reporting_role;
GRANT SELECT ON v_weekly_trend TO reporting_role;
