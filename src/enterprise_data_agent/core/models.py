
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