SELECT
    DATE(timestamp) as day,
    COUNT(DISTINCT user_id) as daily_active_users
FROM events
GROUP BY day
ORDER BY day;
