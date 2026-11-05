-- Remove user_emails that appear in unsubscribers
DELETE e FROM user_emails e
INNER JOIN unsubscribers u ON e.email = u.email;
