import csv
import psycopg2

DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

CSV_PATH = "data/campus_bites_orders.csv"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id            INTEGER PRIMARY KEY,
    order_date          DATE,
    order_time          TIME,
    customer_segment    TEXT,
    order_value         NUMERIC(10, 2),
    cuisine_type        TEXT,
    delivery_time_mins  INTEGER,
    promo_code_used     TEXT,
    is_reorder          TEXT
);
"""

INSERT_ROW = """
INSERT INTO orders (
    order_id, order_date, order_time, customer_segment,
    order_value, cuisine_type, delivery_time_mins, promo_code_used, is_reorder
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (order_id) DO NOTHING;
"""

conn = psycopg2.connect(**DB)
cur = conn.cursor()

cur.execute(CREATE_TABLE)

with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    rows = [
        (
            int(row["order_id"]),
            row["order_date"],
            row["order_time"],
            row["customer_segment"],
            float(row["order_value"]),
            row["cuisine_type"],
            int(row["delivery_time_mins"]),
            row["promo_code_used"],
            row["is_reorder"],
        )
        for row in reader
    ]

cur.executemany(INSERT_ROW, rows)
conn.commit()

print(f"Loaded {cur.rowcount} rows into orders.")

cur.close()
conn.close()
