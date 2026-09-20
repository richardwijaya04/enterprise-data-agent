import duckdb
import pytest

from enterprise_data_agent.tools.quality_profiler import profile_table_quality


@pytest.fixture
def dirty_database():
    con = duckdb.connect(database=":memory:")
    con.execute(""" 
        CREATE TABLE customer_orders (
            order_id VARCHAR,
            user_id VARCHAR,
            amount DOUBLE
        );
        INSERT INTO customer_orders VALUES
            ('ORD_01', 'USR_10', 150.0),
            ('ORD_02', NULL, 200.0),
            ('ORD_03', 'USR_12', NULL),
            ('ORD_01', 'USR_10', 150.0); -- Identical Duplicate            
    """)
    yield con
    con.close()


def test_profile_table_quality(dirty_database):
    report = profile_table_quality(con=dirty_database, table_name="customer_orders")

    assert report.total_rows == 4
    assert report.total_duplicates == 1

    # Check metric user_id column (1 null from 4 rows = 25%)
    user_metric = next(m for m in report.column_metrics if m.column_name == "user_id")

    assert user_metric.null_count == 1
    assert user_metric.null_percentage == 25.0

    # Quality score should be down because duplication and null
    assert report.quality_score < 100.0
