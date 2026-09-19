import duckdb
import pytest

from enterprise_data_agent.core.models import ColumnSchema, TableContract
from enterprise_data_agent.tools.schema_inspector import inspect_schema_drift


@pytest.fixture
def db_connection():
    con = duckdb.connect(database=':memory:')
    yield con
    con.close()
    
@pytest.fixture
def target_contract():
    return TableContract(
        table_name="transactions",
        columns={
            "transaction_id": ColumnSchema(
              name="transaction_id", data_type="VARCHAR", nullable=False  
            ),
            "amount": ColumnSchema(
              name="amount", data_type="DOUBLE", nullable=False  
            ),
            "customer_id": ColumnSchema(
              name="customer_id", data_type="VARCHAR", nullable=False  
            ),
        },
    )
    
def test_schema_drift_detection_success(db_connection, target_contract):
    db_connection.execute("""
        CREATE TABLE transactions (
            transaction_id VARCHAR,
            amount DOUBLE,
            customer_id VARCHAR
        );
    """)
    
    report = inspect_schema_drift(
        con = db_connection,
        table_name = "transactions",
        contract = target_contract,
    )
    
    assert report.is_valid is True
    assert len(report.missing_columns) == 0
    assert len(report.unexpected_columns) == 0
    assert len(report.type_mismatches) == 0
    
def test_schema_drift_detection_with_missmatch(db_connection, target_contract):
    # This test will fail
    db_connection.execute("""
        CREATE TABLE transactions (
            transaction_id VARCHAR,
            amount INTEGER,
            metadata_source VARCHAR
        );
    """)
    
    report = inspect_schema_drift(
        con = db_connection,
        table_name = "transactions",
        contract = target_contract,    
    )
    
    assert report.is_valid is False
    assert "customer_id" in report.missing_columns
    assert "metadata_source" in report.unexpected_columns
    assert "amount" in report.type_mismatches
    assert report.type_mismatches["amount"]["expected"] == "DOUBLE"
    assert report.type_mismatches["amount"]["actual"] == "INTEGER"