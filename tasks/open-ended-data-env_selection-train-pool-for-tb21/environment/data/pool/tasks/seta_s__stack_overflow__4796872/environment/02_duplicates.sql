SELECT a.amount AS a_amount, a.category,
       b.amount AS b_amount, b.status
FROM source_a_transactions a
LEFT JOIN source_b_transactions b ON a.ref_code = b.ref_code
UNION
SELECT a.amount AS a_amount, a.category,
       b.amount AS b_amount, b.status
FROM source_a_transactions a
RIGHT JOIN source_b_transactions b ON a.ref_code = b.ref_code
