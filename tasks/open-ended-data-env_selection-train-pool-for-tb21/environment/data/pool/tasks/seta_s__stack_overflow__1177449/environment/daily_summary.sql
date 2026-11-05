SELECT
    created_at AS txn_date,
    COUNT(*) AS txn_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY created_at
ORDER BY txn_date;
