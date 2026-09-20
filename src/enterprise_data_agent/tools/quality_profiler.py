import duckdb

from enterprise_data_agent.core.models import (
    ColumnQualityMetric,
    DataQualityReport,
)


def profile_table_quality(
    con: duckdb.DuckDBPyConnection, table_name: str
) -> DataQualityReport:
    """Analyzes ratio of data completeness, duplication, and quality score"""
    total_rows = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    if total_rows == 0:
        return DataQualityReport(
            table_name=table_name,
            total_rows=0,
            total_duplicates=0,
            column_metrics=[],
            quality_score=100.0,
        )

    # Detect duplicates based on all columns
    distinct_rows = con.execute(
        f"SELECT COUNT(*) FROM (SELECT DISTINCT * FROM {table_name});"
    ).fetchone()[0]
    duplicates = total_rows - distinct_rows

    # Get metadata name of columns
    columns = [row[0] for row in con.execute(f"DESCRIBE {table_name};").fetchall()]
    col_metrics = []
    total_null_entries = 0

    for col in columns:
        null_count = con.execute(
            f'SELECT COUNT(*) FROM {table_name} WHERE "{col}" IS NULL;'
        ).fetchone()[0]
        null_percentage = round((null_count / total_rows) * 100.0, 2)
        total_null_entries += null_count

        col_metrics.append(
            ColumnQualityMetric(
                column_name=col,
                total_count=total_rows,
                null_count=null_count,
                null_percentage=null_percentage,
            )
        )

    # Formula quality data score
    total_cells = total_rows * len(columns)
    data_loss_ratio = (
        (total_null_entries + (duplicates * len(columns))) / total_cells
        if total_cells > 0
        else 0
    )
    quality_score = max(0.0, round((1.0 - data_loss_ratio) * 100, 2))

    return DataQualityReport(
        table_name=table_name,
        total_rows=total_rows,
        total_duplicates=duplicates,
        column_metrics=col_metrics,
        quality_score=quality_score,
    )
