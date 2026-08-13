# AI Product Analytics Engine
 
A lightweight product analytics engine inspired by tools like PostHog.
 
This project demonstrates how product event data can be ingested, modeled, and queried to answer common product questions — using a minimal, warehouse-first architecture instead of a full analytics platform.
 
---
 
## Quick Start
 
Clone the repo:
 
```
git clone https://github.com/thewrightdata/ai-product-analytics-engine
cd ai-product-analytics-engine
```
 
Install dependencies:
 
```
pip install -r requirements.txt
```
 
(Optional, for the AI query interface) Set up your API key:
 
```
cp .env.example .env
# then edit .env and add your OPENAI_API_KEY
```
 
Run the test suite:
 
```
pytest tests/ -v
```
 
Run analytics:
 
```
python run_queries.py
```
 
(Optional) Ask natural language questions:
 
```
python ai_query.py
```
 
---
 
## Problem
 
Most SaaS products generate large volumes of behavioral event data but lack a simple way to analyze it without standing up a full analytics platform.
 
This project explores a minimal architecture for turning raw product events into actionable insights.
 
---
 
## Architecture
 
```
   Product Events
         │
         ▼
     events.csv
         │
         ▼
       DuckDB
   (analytics warehouse)
         │
         ▼
     SQL Queries
 (funnels, DAU, activation)
         │
         ▼
Insights / Product Metrics
         │
         ▼
  AI Query Interface (natural language → SQL)
```
 
Event data flows into a DuckDB warehouse, gets modeled through typed Python functions with embedded SQL, and can be queried either directly (via `run_queries.py`) or through a natural-language interface.
 
---
 
## Data Model
 
The system operates on a simple event table:
 
| Column     | Description                          |
|------------|---------------------------------------|
| user_id    | Unique identifier for the user        |
| event      | Name of the action performed          |
| timestamp  | When the event occurred               |
 
Each row represents a user performing an action inside a product. Example events include:
 
- `signup`
- `create_project`
- `invite_teammate`
- `view_dashboard`
---
 
## Example Analytics
 
`analytics.py` includes functions for:
 
- **Daily active users** (`daily_active_users`)
- **Activation funnel** (`activation_funnel`)
- **Activation rate** (`activation_rate`)
These demonstrate how product behavior can be analyzed using a warehouse-first approach — each metric is a small, independently tested Python function with its SQL embedded, so it can be reused by both the CLI (`run_queries.py`) and the AI query interface.
 
### Example product questions these answer
 
- How many users signed up this week?
- How many users created a project after signing up?
- What percentage of users activate?
### Example output
 
Running `python run_queries.py`:
 
```
Running analytics queries...
 
--- daily_active_users ---
       day  daily_active_users
2025-01-01                   2
2025-01-02                   1
2025-01-03                   1
 
--- activation_funnel ---
signups=4  created_project=3  invited_teammates=1
```
 
*(Exact numbers will differ based on the contents of `data/events.csv`.)*
 
---
 
## AI Query Interface
 
You can also ask questions about the product data in natural language:
 
```
python ai_query.py
```
 
**Example:**
 
> Question: How many users signed up but never created a project?
 
The system converts the question into SQL, executes it against the event data, and returns the result.
 
Generated SQL for the example above:
 
```sql
SELECT COUNT(DISTINCT user_id)
FROM events
WHERE user_id NOT IN (
    SELECT user_id FROM events WHERE event = 'create_project'
);
```
 
---
 
## Product & Engineering Design Decisions
 
- **DuckDB** was chosen as the analytics engine because it provides a lightweight, zero-infrastructure warehouse that runs entirely locally — no cluster or external service required to demo the concept.
- **Analytics logic lives in typed, testable Python functions (`analytics.py`), with SQL embedded per function**, rather than as standalone `.sql` files. This keeps each metric's query, its output shape, and its test coverage co-located and independently verifiable — the tradeoff favors testability and clear function boundaries over the flexibility of decoupled SQL files.
- **Sample dataset is intentionally small.** The included `events.csv` is illustrative, not a production-scale dataset — it's sized to make the pipeline easy to read and verify end-to-end, not to demonstrate performance at scale.
---
 
## Testing & Reliability
 
The core metrics logic (`analytics.py`) and the SQL-safety helpers in
`ai_query.py` are covered by a pytest suite in `tests/`, run automatically
on every push via GitHub Actions:
 
```
pytest tests/ -v
```
 
What's covered:
 
- Schema and data validation (`load_events` rejects missing columns or an empty file)
- Correctness of each metric (signups, activation funnel, activation rate, DAU) against a known fixture dataset
- Edge cases (e.g. activation rate when there are zero signups)
- The AI query interface's SQL-cleaning and read-only safety check, so a malformed or unsafe model response can't reach the database
The `ai_query.py` interface also defensively rejects any generated SQL that isn't a plain `SELECT`, since the query text comes from an LLM and shouldn't be trusted to only ever produce read-only statements.
 
---
 
## Known Limitations & Next Steps
 
This is a prototype, and the following are gaps I'd address before treating it as production-ready:
 
- **Single flat event table.** Next step: normalize into a proper dimensional model (e.g. separate `users` and `events` tables) as the schema grows.
- **No CI-enforced linting/type checking.** Next step: add `ruff` and `mypy` to the GitHub Actions workflow alongside the test run.
- **AI query interface only supports single-table questions.** Next step: extend the schema description in the prompt as the data model grows past one table.
### Other future extensions
 
- Streaming event ingestion
- Retention cohort analysis
- Session replay integration
---
 
## License
 
MIT
 
