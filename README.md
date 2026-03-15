# Mini Product Analytics Engine

A lightweight product analytics engine inspired by tools like PostHog.

This project demonstrates how product event data can be ingested, modeled, and queried to answer common product questions.

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

## Product Design Decisions

This project intentionally uses a warehouse-first architecture.

Rather than building custom analytics logic in application code, events are stored in DuckDB and queried using SQL. This mirrors the approach used by modern analytics platforms where the warehouse becomes the source of truth.

DuckDB was chosen because it allows the entire analytics pipeline to run locally with zero infrastructure.
