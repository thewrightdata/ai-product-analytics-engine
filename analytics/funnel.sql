SELECT
    COUNT(DISTINCT CASE WHEN event='signup' THEN user_id END) as signups,
    COUNT(DISTINCT CASE WHEN event='create_project' THEN user_id END) as created_project,
    COUNT(DISTINCT CASE WHEN event='invite_teammate' THEN user_id END) as invited_teammates
FROM events;
