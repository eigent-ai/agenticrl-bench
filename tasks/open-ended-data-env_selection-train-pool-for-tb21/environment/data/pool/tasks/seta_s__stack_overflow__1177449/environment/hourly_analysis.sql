SELECT
    to_char(created_at, 'HH') AS hour_of_day,
    COUNT(*) AS txn_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY to_char(created_at, 'HH')
ORDER BY hour_of_day;
