"""
Query Models.

This module contains Pydantic models for natural language queries,
SQL queries, and query results.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


class NaturalLanguageQuery(BaseModel):
    """
    Natural language query request model.

    Attributes
    ----------
    query : str
        Natural language query text.
    visualization_type : Optional[str]
        Preferred visualization type (bar, line, pie, table).
    max_results : Optional[int]
        Maximum number of results to return.

    Examples
    --------
    >>> query = NaturalLanguageQuery(
    ...     query="Show me top 10 customers by sales",
    ...     visualization_type="bar"
    ... )
    """

    query: str = Field(
        ...,
        description="Natural language query",
        min_length=3,
        max_length=1000,
        example="Show me the top 10 best-selling artists",
    )
    visualization_type: Optional[str] = Field(
        default="table",
        description="Preferred visualization type",
        example="bar",
    )
    max_results: Optional[int] = Field(
        default=100,
        description="Maximum number of results to return",
        ge=1,
        le=1000,
    )

    @validator("visualization_type")
    def validate_visualization_type(cls, v):
        """
        Validate visualization type.

        Parameters
        ----------
        v : str or None
            Visualization type.

        Returns
        -------
        str or None
            Validated visualization type.

        Raises
        ------
        ValueError
            If visualization type is not supported.
        """
        if v is None:
            return v
        allowed_types = ["bar", "line", "pie", "table", "scatter", "area"]
        if v.lower() not in allowed_types:
            raise ValueError(
                f"Visualization type must be one of {allowed_types}, got {v}"
            )
        return v.lower()


class QueryRequest(BaseModel):
    """
    Query request model with optional SQL override.

    Attributes
    ----------
    natural_language_query : Optional[str]
        Natural language query text.
    sql_query : Optional[str]
        Direct SQL query (overrides natural language).
    visualization_type : Optional[str]
        Preferred visualization type.
    max_results : Optional[int]
        Maximum number of results to return.

    Examples
    --------
    >>> request = QueryRequest(
    ...     natural_language_query="Show total sales by country",
    ...     visualization_type="pie"
    ... )
    """

    natural_language_query: Optional[str] = Field(
        default=None,
        description="Natural language query",
        example="What are the total sales by country?",
    )
    sql_query: Optional[str] = Field(
        default=None,
        description="Direct SQL query",
        example="SELECT Country, SUM(Total) FROM invoices GROUP BY Country",
    )
    visualization_type: Optional[str] = Field(
        default="table", description="Preferred visualization type"
    )
    max_results: Optional[int] = Field(default=100, ge=1, le=1000)

    @validator("sql_query", "natural_language_query")
    def validate_query(cls, v, values, field):
        """
        Validate that at least one query type is provided.

        Parameters
        ----------
        v : str or None
            Query value.
        values : dict
            All field values.
        field : Field
            Field being validated.

        Returns
        -------
        str or None
            Validated query value.

        Raises
        ------
        ValueError
            If neither query type is provided.
        """
        if field.name == "natural_language_query":
            if not v and not values.get("sql_query"):
                raise ValueError(
                    "Either natural_language_query or sql_query must be provided"
                )
        return v


class QueryResult(BaseModel):
    """
    Query execution result model.

    Attributes
    ----------
    columns : List[str]
        Column names in the result set.
    rows : List[List[Any]]
        Result rows as list of lists.
    row_count : int
        Number of rows returned.
    execution_time_ms : float
        Query execution time in milliseconds.

    Examples
    --------
    >>> result = QueryResult(
    ...     columns=["Country", "Total"],
    ...     rows=[["USA", 1234.56], ["Canada", 890.12]],
    ...     row_count=2,
    ...     execution_time_ms=45.2
    ... )
    """

    columns: List[str] = Field(..., description="Column names")
    rows: List[List[Any]] = Field(..., description="Result rows")
    row_count: int = Field(..., description="Number of rows", ge=0)
    execution_time_ms: float = Field(
        ..., description="Execution time in milliseconds", ge=0
    )


class QueryResponse(BaseModel):
    """
    Complete query response model.

    Attributes
    ----------
    success : bool
        Whether the query executed successfully.
    natural_language_query : Optional[str]
        Original natural language query.
    generated_sql : Optional[str]
        Generated or provided SQL query.
    result : Optional[QueryResult]
        Query execution result.
    error : Optional[str]
        Error message if query failed.
    suggested_visualization : Optional[str]
        Suggested visualization type based on data.
    metadata : Optional[Dict[str, Any]]
        Additional metadata about the query.

    Examples
    --------
    >>> response = QueryResponse(
    ...     success=True,
    ...     natural_language_query="Show top customers",
    ...     generated_sql="SELECT * FROM customers LIMIT 10",
    ...     result=result,
    ...     suggested_visualization="table"
    ... )
    """

    success: bool = Field(..., description="Query execution success status")
    natural_language_query: Optional[str] = Field(
        default=None, description="Original natural language query"
    )
    generated_sql: Optional[str] = Field(default=None, description="Generated SQL")
    result: Optional[QueryResult] = Field(default=None, description="Query result")
    error: Optional[str] = Field(default=None, description="Error message")
    suggested_visualization: Optional[str] = Field(
        default=None, description="Suggested visualization type"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class QueryHistory(BaseModel):
    """
    Query history record model.

    Attributes
    ----------
    id : Optional[int]
        Unique identifier for the query.
    natural_language_query : str
        Original natural language query.
    generated_sql : str
        Generated SQL query.
    execution_time_ms : float
        Query execution time in milliseconds.
    row_count : int
        Number of rows returned.
    success : bool
        Whether the query executed successfully.
    error : Optional[str]
        Error message if query failed.
    created_at : datetime
        Timestamp when the query was executed.

    Examples
    --------
    >>> history = QueryHistory(
    ...     id=1,
    ...     natural_language_query="Show top artists",
    ...     generated_sql="SELECT * FROM artists LIMIT 10",
    ...     execution_time_ms=23.5,
    ...     row_count=10,
    ...     success=True,
    ...     created_at=datetime.now()
    ... )
    """

    id: Optional[int] = Field(default=None, description="Query ID")
    natural_language_query: str = Field(..., description="Natural language query")
    generated_sql: str = Field(..., description="Generated SQL")
    execution_time_ms: float = Field(..., description="Execution time in ms", ge=0)
    row_count: int = Field(..., description="Number of rows", ge=0)
    success: bool = Field(..., description="Success status")
    error: Optional[str] = Field(default=None, description="Error message")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}
