# Campus Bites — Local Postgres Setup

A local Postgres database for the Campus Bites orders dataset, running in Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)

## Quickstart

```bash
# From the project root
docker compose up -d
```

On first startup, Postgres will automatically run `init.sql`, which creates the `orders` table and loads the CSV. This takes a few seconds.

## Connect

**psql (terminal):**
```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

**Any SQL client** (TablePlus, DBeaver, DataGrip, etc.):

| Setting  | Value       |
|----------|-------------|
| Host     | localhost   |
| Port     | 5432        |
| Database | campus_bites |
| User     | postgres    |
| Password | postgres    |

## Sample Queries

```sql
-- Preview data
SELECT * FROM orders LIMIT 10;

-- Orders by cuisine type
SELECT cuisine_type, COUNT(*) AS orders, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY cuisine_type
ORDER BY orders DESC;

-- Promo code usage by segment
SELECT customer_segment, promo_code_used, COUNT(*) AS total
FROM orders
GROUP BY customer_segment, promo_code_used
ORDER BY customer_segment;
```

## Reset the Database

To wipe the database and reload from scratch (re-runs `init.sql`):

```bash
docker compose down -v
docker compose up -d
```

## Stop (keep data)

```bash
docker compose down
```

Data persists in a Docker volume (`postgres_data`) and will be available on next `docker compose up -d`.

## Project Structure

```
.
├── docker-compose.yml   # Postgres service definition
├── init.sql             # Table creation + CSV load (runs on first startup)
├── data/
│   └── campus_bites_orders.csv
└── README.md
```
