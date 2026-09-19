import duckdb

from enterprise_data_agent.core.models import (
    SchemaDriftReport,
    TableContract,
)


def inspect_schema_drift(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    contract: TableContract,
) -> SchemaDriftReport:
    """ Validate the schema of a table against a given contract. """
    query = f"DESCRIBE {table_name};"
    raw_schema = con.execute(query).fetchall()
    
    actual_columns = {row[0]: row[1] for row in raw_schema}
    expected_columns = contract.columns
    
    missing_cols = [
        col for col in expected_columns if col not in actual_columns
    ]
    unexpected_cols = [
        col for col in actual_columns if col not in expected_columns
    ]
    
    type_mismatches = {}
    for col_name, col_def in expected_columns.items():
        if col_name in actual_columns:
            actual_type = actual_columns[col_name].upper()
            expected_type = col_def.data_type.upper()
            if actual_type != expected_type:
                type_mismatches[col_name] = {
                    "expected": expected_type,
                    "actual": actual_type,
                }
    is_valid = (
        len(missing_cols) == 0
        and len(unexpected_cols) == 0
        and len(type_mismatches) == 0
    )
    
    return SchemaDriftReport(
        is_valid=is_valid,
        missing_columns=missing_cols,
        unexpected_columns=unexpected_cols,
        type_mismatches=type_mismatches,   
    )