import duckdb
from fastmcp import FastMCP

from enterprise_data_agent.core.models import ColumnSchema, TableContract
from enterprise_data_agent.tools.schema_inspector import inspect_schema_drift

# Inisialisasi Server MCP
mcp = FastMCP("Enterprise-Data-Governance-Agent")


@mcp.tool()
def validate_table_schema(
    database_path: str,
    table_name: str,
    expected_columns: dict[str, str],
) -> dict:
    """
    Validate the schema of a table in a DuckDB database against an expected contract.
    Args:
        database_path (str): Path to the DuckDB database file.
        table_name (str): Name of the table to validate.
        expected_columns (dict[str, str]): A dictionary where keys are column names and values are
    """
    con = duckdb.connect(database=database_path)
    try:
        # Reconstruct the data contract from the LLM input
        columns_dict = {
            col: ColumnSchema(name=col, data_type=dtype.upper())
            for col, dtype in expected_columns.items()
        }
        contract = TableContract(table_name=table_name, columns=columns_dict)

        report = inspect_schema_drift(con, table_name, contract)
        return report.model_dump()
    finally:
        con.close()


if __name__ == "__main__":
    mcp.run()