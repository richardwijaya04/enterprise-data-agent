def test_environment_is_ready():
    """Verify that the testing environment and core libraries are ready."""
    import duckdb
    import pydantic

    con = duckdb.connect(database=":memory:")
    result = con.execute("SELECT 42 AS answer").fetchone()
    assert result[0] == 42, "DuckDB execution failed"
    assert pydantic.__version__ is not None, "Pydantic is not installed"
