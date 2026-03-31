# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A local PostgreSQL pipeline for the Campus Bites orders dataset. The database runs in Docker; a Python script handles table creation and data loading from CSV.

## Setup

```bash
# Start the database
docker compose up -d

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install psycopg2-binary

# Load data into the orders table
python load_orders.py
```

## Common Commands

```bash
# Open a psql session
docker exec -it campus_bites_db psql -U postgres -d campus_bites

# Stop the database (data persists in the postgres_data volume)
docker compose down

# Wipe and recreate the database from scratch
docker compose down -v && docker compose up -d
```

## Database

| Setting  | Value         |
|----------|---------------|
| Host     | localhost     |
| Port     | 5432          |
| Database | campus_bites  |
| User     | postgres      |
| Password | postgres      |

## Architecture

- **`docker-compose.yml`** — runs `postgres:16` as `campus_bites_db`, persisting data in a named volume (`postgres_data`). The CSV is mounted at `/data/campus_bites_orders.csv` inside the container.
- **`load_orders.py`** — creates the `orders` table if it doesn't exist, then bulk-inserts from `data/campus_bites_orders.csv` using `psycopg2`. Re-running is safe; duplicate `order_id`s are skipped via `ON CONFLICT DO NOTHING`.
- **`data/campus_bites_orders.csv`** — source dataset (~1300 rows) with fields: `order_id`, `order_date`, `order_time`, `customer_segment`, `order_value`, `cuisine_type`, `delivery_time_mins`, `promo_code_used`, `is_reorder`.

> Note: there is no `init.sql`. The database starts empty; `load_orders.py` must be run to create and populate the `orders` table.
