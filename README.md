# AI Product Analytics Engine

A lightweight product analytics engine inspired by tools like PostHog.

This project demonstrates how product event data can be ingested, modeled, and queried to answer common product questions.

---

## Quick Start

Clone the repo:

git clone https://github.com/thewrightdata/ai-product-analytics-engine
cd ai-product-analytics-engine

Install dependencies:

pip install -r requirements.txt

Run analytics:

python run_queries.py

(Optional) Ask natural language questions:

python ai_query.py

---

## Problem

Most SaaS products generate large volumes of behavioral event data but lack a simple way to analyze it without a full analytics platform.

This project explores a minimal architecture for turning raw product events into actionable insights.

---

## Running the project

1. Install dependencies

pip install -r requirements.txt

2. Run the analytics pipeline

python run_queries.py

This will load the event dataset into DuckDB and execute the example analytics queries.

The output includes:
- Daily active users
- Activation funnel
- Activation rate

---

## Architecture

Event data → DuckDB warehouse → SQL analytics layer → AI query interface

The goal is to show how a small set of components can support common product analytics workflows.

---

## Data Model

The system operates on a simple event table:

events

user_id  
event  
timestamp  

Each row represents a user performing an action inside a product.

Example events include:

- signup
- create_project
- invite_teammate
- view_dashboard

---

## Example Analytics

The repository includes example SQL queries for:

Daily active users  
Activation funnels  
Activation rate

These queries demonstrate how product behavior can be analyzed using a warehouse-first approach.

---

## Example Product Questions

How many users signed up this week?

How many users created a project after signing up?

What percentage of users activate?

---

## Future Improvements

Possible extensions include:

- streaming event ingestion
- retention cohort analysis

---

- ## System Architecture

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

- session replay integration
- AI-generated SQL queries

---

## AI Query Interface

You can ask questions about the product data using natural language.

Example:

How many users signed up but never created a project?

Run:

python ai_query.py

The system will:
1. Convert the question into SQL
2. Execute the query against the event data
3. Return the result

$ python ai_query.py

Question: How many users signed up but never created a project?

Generated SQL:

SELECT COUNT(DISTINCT user_id)
FROM events
WHERE user_id NOT IN (
    SELECT user_id FROM events WHERE event = 'create_project'
);

## Example Output

Daily Active Users

2025-01-01 | 3
2025-01-02 | 4

---

## Product Design Decisions

DuckDB was chosen as the analytics engine because it provides a lightweight, zero-infrastructure warehouse that can run locally.

Analytics logic is stored in SQL files rather than Python to mirror how modern data teams organize transformation layers.

This structure allows queries to evolve independently of application logic.
