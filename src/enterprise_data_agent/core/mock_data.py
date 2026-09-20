from pathlib import Path

import duckdb

DATA_DIR = Path("data")


def generate_mock_datasets() -> None:
    """Generate sample Paquet datasets for multi-industry"""
    DATA_DIR.mkdir(exist_ok=True)
    con = duckdb.connect(database=":memory:")

    # 1. Tech / E-commerce dataset (user activity logs)
    con.execute("""
       CREATE TABLE tech_events AS SELECT * FROM (
           VALUES
                (101, 'user_click', '2026-09-01 10:00:00', 'US', NULL),
                (102, 'checkout', '2026-09-01 10:05:00', 'AU', 'user_102@email.com'),
                (103, 'page_view', 'invalid_date', 'SG', 'user_103@email.com')
       )   AS t(user_id, event_type, timestamp, country, email);
    """)
    con.execute(
        f"COPY tech_events TO '{DATA_DIR} / 'tech_events.parquet' (FORMAT PARQUET);"
    )

    # 2. FMCG / Retail Dataset (Inventory & Stock Analytics)
    con.execute("""
        CREATE TABLE fmcg_inventory AS SELECT * FROM (
            VALUES 
                ('SKU-001', 'UHT Milk 1L', 500, 15.00, '2026-12-31'),
                ('SKU-002', 'Chocolate Biscuits', -10, 8.00, '2026-10-15'),
                ('SKU-003', 'Cooking Oil 2L', 200, NULL, '2027-01-01')
        ) AS t(sku, product_name, stock_qty, unit_price, expiry_date);
    """)
    con.execute(
        f"COPY fmcg_inventory TO '{DATA_DIR}/fmcg_inventory.parquet' (FORMAT PARQUET);"
    )

    con.close()


if __name__ == "__main__":
    generate_mock_datasets()
