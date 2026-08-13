"""
Core analytics functions for the product analytics engine.

Loads product event data into a DuckDB warehouse and exposes a small set
of metrics functions (signups, activation funnel, DAU) that can be reused
by both the CLI script (run_queries.py) and the test suite.
"""

import duckdb
import pandas as pd

EVENTS_SCHEMA = {"user_id", "event", "timestamp"}


def load_events(csv_path: str = "data/events.csv") -> pd.DataFrame:
    """Load and lightly validate the raw events CSV."""
    df = pd.read_csv(csv_path)

    missing = EVENTS_SCHEMA - set(df.columns)
    if missing:
        raise ValueError(f"events.csv is missing required column(s): {missing}")

    if df.empty:
        raise ValueError("events.csv contains no rows")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def get_connection(df: pd.DataFrame, db_path: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """Create a DuckDB connection with the events table loaded.

    Defaults to an in-memory database so tests and repeated runs don't
    depend on (or mutate) a shared analytics.db file on disk.
    """
    con = duckdb.connect(db_path)
    con.execute("CREATE OR REPLACE TABLE events AS SELECT * FROM df")
    return con


def total_signups(con: duckdb.DuckDBPyConnection) -> int:
    """Count of distinct users who have a 'signup' event."""
    result = con.execute(
        "SELECT COUNT(DISTINCT user_id) FROM events WHERE event = 'signup'"
    ).fetchone()
    return result[0]


def activation_funnel(con: duckdb.DuckDBPyConnection) -> dict:
    """Distinct-user counts for signup -> create_project -> invite_teammate."""
    row = con.execute("""
        SELECT
            COUNT(DISTINCT CASE WHEN event = 'signup' THEN user_id END) AS signups,
            COUNT(DISTINCT CASE WHEN event = 'create_project' THEN user_id END) AS created_project,
            COUNT(DISTINCT CASE WHEN event = 'invite_teammate' THEN user_id END) AS invited_teammates
        FROM events
    """).fetchone()
    return {
        "signups": row[0],
        "created_project": row[1],
        "invited_teammates": row[2],
    }


def activation_rate(con: duckdb.DuckDBPyConnection) -> float:
    """Share of signed-up users who went on to create a project (0.0-1.0)."""
    funnel = activation_funnel(con)
    if funnel["signups"] == 0:
        return 0.0
    return funnel["created_project"] / funnel["signups"]


def daily_active_users(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Distinct active users per calendar day."""
    return con.execute("""
        SELECT
            CAST(timestamp AS DATE) AS day,
            COUNT(DISTINCT user_id) AS daily_active_users
        FROM events
        GROUP BY 1
        ORDER BY 1
    """).fetchdf()


if __name__ == "__main__":
    events_df = load_events()
    conn = get_connection(events_df)

    print(f"Total signups: {total_signups(conn)}")
    print("Funnel results:", activation_funnel(conn))
    print(f"Activation rate: {activation_rate(conn):.1%}")
