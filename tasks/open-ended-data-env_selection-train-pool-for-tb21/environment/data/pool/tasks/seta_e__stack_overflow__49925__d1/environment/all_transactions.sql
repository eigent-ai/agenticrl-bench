SELECT product, amount, date FROM transactions_east
UNION
SELECT product, amount, date FROM transactions_west
ORDER BY date, product;
