"""
CLI entry point: runs the example analytics queries against data/events.csv
and prints the results. See README.md for expected output.
"""

from analytics import (
    load_events,
    get_connection,
    daily_active_users,
    activation_funnel,
)


def main():
    print("Running analytics queries...\n")

    events_df = load_events()
    con = get_connection(events_df)

    print("--- daily_active_users.sql ---")
    print(daily_active_users(con).to_string(index=False))

    print("\n--- funnel.sql ---")
    funnel = activation_funnel(con)
    print(f"signups={funnel['signups']}  "
          f"created_project={funnel['created_project']}  "
          f"invited_teammates={funnel['invited_teammates']}")


if __name__ == "__main__":
    main()
