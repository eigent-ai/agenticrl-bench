UPDATE articles
SET body = REPLACE(body, '&amp;', '&');
