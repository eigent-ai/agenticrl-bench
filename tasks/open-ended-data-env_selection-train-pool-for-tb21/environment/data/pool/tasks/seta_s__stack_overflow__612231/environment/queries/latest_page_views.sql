SELECT *, MAX(view_time) FROM page_views GROUP BY user_id, page_id ORDER BY view_time DESC;
