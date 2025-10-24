"""
Schema Models.

This module contains Pydantic models for database schema representation
and documentation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ColumnInfo(BaseModel):
    """
    Database column information model.

    Attributes
    ----------
    name : str
        Column name.
    type : str
        Column data type.
    nullable : bool
        Whether the column accepts NULL values.
    default : Optional[Any]
        Default value for the column.
    primary_key : bool
        Whether this column is part of the primary key.
    foreign_key : Optional[Dict[str, str]]
        Foreign key reference if applicable.

    Examples
    --------
    >>> column = ColumnInfo(
    ...     name="CustomerId",
    ...     type="INTEGER",
    ...     nullable=False,
    ...     primary_key=True
    ... )
    """

    name: str = Field(..., description="Column name")
    type: str = Field(..., description="Column data type")
    nullable: bool = Field(..., description="Whether column accepts NULL")
    default: Optional[Any] = Field(default=None, description="Default value")
    primary_key: bool = Field(default=False, description="Is primary key")
    foreign_key: Optional[Dict[str, str]] = Field(
        default=None,
        description="Foreign key reference",
        example={"table": "artists", "column": "ArtistId"},
    )


class TableSchema(BaseModel):
    """
    Database table schema model.

    Attributes
    ----------
    name : str
        Table name.
    columns : List[ColumnInfo]
        List of column information.
    primary_keys : List[str]
        List of primary key column names.
    foreign_keys : List[Dict[str, Any]]
        List of foreign key relationships.
    row_count : Optional[int]
        Approximate number of rows in the table.
    description : Optional[str]
        Human-readable table description.

    Examples
    --------
    >>> table = TableSchema(
    ...     name="customers",
    ...     columns=[column1, column2],
    ...     primary_keys=["CustomerId"],
    ...     row_count=1000
    ... )
    """

    name: str = Field(..., description="Table name")
    columns: List[ColumnInfo] = Field(..., description="Column information")
    primary_keys: List[str] = Field(default_factory=list, description="Primary keys")
    foreign_keys: List[Dict[str, Any]] = Field(
        default_factory=list, description="Foreign key relationships"
    )
    row_count: Optional[int] = Field(
        default=None, description="Approximate row count"
    )
    description: Optional[str] = Field(
        default=None, description="Table description"
    )


class DatabaseSchema(BaseModel):
    """
    Complete database schema model.

    Attributes
    ----------
    tables : List[TableSchema]
        List of table schemas.
    table_count : int
        Total number of tables.
    relationships : List[Dict[str, Any]]
        List of relationships between tables.
    database_type : str
        Type of database (sqlite, postgresql, mysql, etc.).
    version : Optional[str]
        Database version.

    Examples
    --------
    >>> schema = DatabaseSchema(
    ...     tables=[table1, table2],
    ...     table_count=2,
    ...     relationships=[],
    ...     database_type="sqlite"
    ... )
    """

    tables: List[TableSchema] = Field(..., description="List of tables")
    table_count: int = Field(..., description="Total number of tables", ge=0)
    relationships: List[Dict[str, Any]] = Field(
        default_factory=list, description="Table relationships"
    )
    database_type: str = Field(..., description="Database type")
    version: Optional[str] = Field(default=None, description="Database version")


class SchemaResponse(BaseModel):
    """
    Schema API response model.

    Attributes
    ----------
    success : bool
        Whether the schema retrieval was successful.
    schema : Optional[DatabaseSchema]
        Database schema information.
    error : Optional[str]
        Error message if retrieval failed.

    Examples
    --------
    >>> response = SchemaResponse(
    ...     success=True,
    ...     schema=database_schema
    ... )
    """

    success: bool = Field(..., description="Success status")
    schema: Optional[DatabaseSchema] = Field(
        default=None, description="Database schema"
    )
    error: Optional[str] = Field(default=None, description="Error message")


class TableSuggestion(BaseModel):
    """
    Table suggestion model for query assistance.

    Attributes
    ----------
    table_name : str
        Name of the suggested table.
    relevance_score : float
        Relevance score (0-1).
    sample_queries : List[str]
        Sample queries for this table.
    description : str
        Description of what this table contains.

    Examples
    --------
    >>> suggestion = TableSuggestion(
    ...     table_name="customers",
    ...     relevance_score=0.95,
    ...     sample_queries=["Show all customers from USA"],
    ...     description="Customer information and contact details"
    ... )
    """

    table_name: str = Field(..., description="Table name")
    relevance_score: float = Field(
        ..., description="Relevance score", ge=0.0, le=1.0
    )
    sample_queries: List[str] = Field(
        default_factory=list, description="Sample queries"
    )
    description: str = Field(..., description="Table description")
