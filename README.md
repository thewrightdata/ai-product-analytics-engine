# Mini Product Analytics Engine

A lightweight product analytics engine inspired by tools like PostHog.

This project demonstrates how product event data can be transformed into actionable insights using a simple analytics stack.

## Features

- Event ingestion pipeline
- SQL-based product analytics
- Funnel analysis
- User retention analysis
- Natural language → SQL queries

## Architecture

Events → DuckDB → SQL metrics → AI query layer

## Example Questions

- How many users signed up this week?
- How many users created a project after signing up?
- What percentage of users activate?

## Tech Stack

- Python
- DuckDB
- SQL
- OpenAI API

## Why this project exists

Most SaaS products generate massive amounts of event data but struggle to turn it into insights quickly. This project explores a minimal architecture for building a product analytics system from scratch.
