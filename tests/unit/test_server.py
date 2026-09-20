import duckdb

from enterprise_data_agent.server import validate_table_schema


def test_validate_table_schema_tool(tmp_path):
    # Create a temporary duckdb database for real-world solution
    db_file = str (tmp_path / "test_warehouse.duckdb")
    con = duckdb.connect(database=db_file)
    con.execute("""
        CREATE TABLE customers (
            customer_id VARCHAR,
            age INTEGER,
            signup_date TIMESTAMP
        );
    """)
    con.close()
    
    # Call the MCP tool
    result = validate_table_schema(
        database_path=db_file,
        table_name="customers",
        expected_columns={"customer_id": "VARCHAR", "age": "INTEGER"},
    )
    
    # Verify detection of unexpected columns (signup_date)
    assert result["is_valid"] is False
    assert "signup_date" in result["unexpected_columns"]
    assert len(result["missing_columns"]) == 0
    