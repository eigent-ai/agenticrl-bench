SELECT email, COUNT(*) as cnt FROM users GROUP BY email HAVING cnt > 1
