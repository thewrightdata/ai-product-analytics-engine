WITH first_signup AS (
    SELECT user_id, MIN(timestamp) AS signup_time
    FROM events
    WHERE event = 'signup'
    GROUP BY user_id
)

SELECT
    COUNT(DISTINCT e.user_id) AS returning_users
FROM events e
JOIN first_signup s ON e.user_id = s.user_id
WHERE e.timestamp > s.signup_time;
