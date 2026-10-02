import duckdb


def generate_mock_warehouse(db_path: str = "enterprise_warehouse.duckdb") -> None:
    """Make baseline warehouse."""
    con = duckdb.connect(database=db_path)

    # 1. Tabel Transaksi Bersih (Baseline)
    con.execute("""
        CREATE OR REPLACE TABLE clean_transactions AS
        SELECT 
            'TXN_' || LPAD(range::VARCHAR, 5, '0') AS transaction_id,
            'USR_' || LPAD((range % 50)::VARCHAR, 4, '0') AS user_id,
            ROUND(random() * 1000 + 10, 2) AS amount,
            CURRENT_DATE - (range % 30) AS transaction_date
        FROM range(100);
    """)

    # 2. Tabel Rusak: Mengalami Schema Drift & Nilai Rusak
    con.execute("""
        CREATE OR REPLACE TABLE drifted_orders AS
        SELECT 
            'ORD_' || LPAD(range::VARCHAR, 5, '0') AS order_id,
            CASE WHEN range % 5 = 0 THEN NULL ELSE 'CUST_' || range END AS customer_ref,
            (random() * 500)::INTEGER AS amount -- Tipe INTEGER, bukan DOUBLE
        FROM range(50);
    """)

    con.close()


if __name__ == "__main__":
    generate_mock_warehouse()
    print("Mock database created successfully.")
