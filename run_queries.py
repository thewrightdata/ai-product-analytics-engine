import duckdb
import pandas as pd
from pathlib import Path

# Load event data
df = pd.read_csv("data/events.csv")

# Connect to DuckDB
con = duckdb.connect("analytics.db")
con.execute("CREATE OR REPLACE TABLE events AS SELECT * FROM df")

# Find all SQL files
queries_path = Path("analytics")
sql_files = list(queries_path.glob("*.sql"))

print("\nRunning analytics queries...\n")

for sql_file in sql_files:
    print(f"--- {sql_file.name} ---")
    query = sql_file.read_text()

    try:
        result = con.execute(query).fetchdf()
        print(result)
        print()
    except Exception as e:
        print("Error:", e)
