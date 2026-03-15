import duckdb
import pandas as pd

# Load events
df = pd.read_csv("data/events.csv")

# Create database
con = duckdb.connect("analytics.db")
con.execute("CREATE OR REPLACE TABLE events AS SELECT * FROM df")

# Example metric: total users who signed up
signups = con.execute("""
SELECT COUNT(DISTINCT user_id)
FROM events
WHERE event = 'signup'
""").fetchone()[0]

print(f"Total signups: {signups}")

# Example funnel
funnel = con.execute("""
SELECT
    COUNT(DISTINCT CASE WHEN event='signup' THEN user_id END) as signups,
    COUNT(DISTINCT CASE WHEN event='create_project' THEN user_id END) as created_project
FROM events
""").fetchall()

print("Funnel results:", funnel)
