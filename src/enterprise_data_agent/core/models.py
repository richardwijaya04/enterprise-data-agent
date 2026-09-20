from pydantic import BaseModel, Field


class ColumnSchema(BaseModel):
    name: str
    data_type: str
    nullable: bool = True


class TableContract(BaseModel):
    table_name: str
    columns: dict[str, ColumnSchema]
    primary_key: str | None = None


class SchemaDriftReport(BaseModel):
    is_valid: bool
    missing_columns: list[str] = Field(default_factory=list)
    unexpected_columns: list[str] = Field(default_factory=list)
    type_mismatches: dict[str, dict[str, str]] = Field(default_factory=dict)


# Privacy Data
class PIIEntity(BaseModel):
    entity_type: str
    original_value: str
    masked_value: str


class PIIScanResult(BaseModel):
    has_pii: bool
    entities_count: int
    detected_entities: list[PIIEntity]
    sanitized_text: str


# Automated Data Quality Profiler
class ColumnQualityMetric(BaseModel):
    column_name: str
    total_count: int
    null_count: int
    null_percentage: float


class DataQualityReport(BaseModel):
    table_name: str
    total_rows: int
    total_duplicates: int
    column_metrics: list[ColumnQualityMetric]
    quality_score: float
