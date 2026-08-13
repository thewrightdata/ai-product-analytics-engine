"""
Natural-language query interface: converts a plain-English question into
SQL via an LLM, then runs it against the events table.

Requires OPENAI_API_KEY to be set in the environment (see .env.example).
"""

import os
import re
import sys

from openai import OpenAI

from analytics import load_events, get_connection

SCHEMA_DESCRIPTION = "events(user_id INTEGER, event TEXT, timestamp TIMESTAMP)"

# Only allow read-only queries — this is a demo query interface, not a
# general-purpose SQL executor, so we defensively block anything that
# could mutate the database even if the model were prompted to do so.
BLOCKED_KEYWORDS = ("insert", "update", "delete", "drop", "alter", "create", "attach")


def get_client() -> OpenAI:
    """Build an OpenAI client, failing fast with a clear message if the
    API key isn't configured rather than a raw auth error mid-request."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit(
            "Error: OPENAI_API_KEY is not set.\n"
            "Copy .env.example to .env, add your key, and re-run "
            "(or `export OPENAI_API_KEY=...` directly)."
        )
    return OpenAI(api_key=api_key)


def clean_sql(raw_text: str) -> str:
    """Strip markdown code fences and leading/trailing whitespace from a
    model response. Models frequently wrap SQL in ```sql ... ``` even
    when told not to, and an un-stripped fence causes duckdb to error
    on a query that is otherwise perfectly valid."""
    text = raw_text.strip()
    text = re.sub(r"^```(?:sql)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def is_safe_query(sql: str) -> bool:
    """Reject anything that isn't a read-only SELECT."""
    lowered = sql.strip().lower()
    if not lowered.startswith("select"):
        return False
    return not any(keyword in lowered for keyword in BLOCKED_KEYWORDS)


def ask(question: str, client: OpenAI, con) -> str:
    """Generate SQL for a natural-language question and execute it."""
    prompt = f"""You are a data analyst.
Table schema:
{SCHEMA_DESCRIPTION}

Write a single read-only SQL SELECT query that answers the question.
Return SQL only, with no markdown formatting or explanation.

Question:
{question}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    sql_query = clean_sql(response.choices[0].message.content)
    print(f"\nGenerated SQL:\n{sql_query}")

    if not is_safe_query(sql_query):
        return "Refused to execute: query did not pass the read-only safety check."

    try:
        result = con.execute(sql_query).fetchdf()
        return result.to_string(index=False)
    except Exception as exc:
        return f"Query failed: {exc}"


def main():
    client = get_client()
    events_df = load_events()
    con = get_connection(events_df)

    print("Ask a question about the product data.\n")
    question = input("Question: ")
    print("\nResult:\n")
    print(ask(question, client, con))


if __name__ == "__main__":
    main()
