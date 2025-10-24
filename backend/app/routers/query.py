"""
Query Router.

This module defines API endpoints for processing natural language queries
and executing SQL statements.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import io

from app.models.query import (
    NaturalLanguageQuery,
    QueryRequest,
    QueryResponse,
    QueryResult,
)
from app.services import NLToSQLService, QueryExecutor
from app.config import get_settings

router = APIRouter(prefix="/api/query", tags=["query"])
settings = get_settings()

# Initialize services (can be moved to dependency injection)
nl_to_sql_service = NLToSQLService()
query_executor = QueryExecutor()


@router.post("/nl", response_model=QueryResponse)
async def process_natural_language_query(query: NaturalLanguageQuery):
    """
    Process a natural language query and return results.

    This endpoint converts natural language to SQL, executes the query,
    and returns formatted results with visualization suggestions.

    Parameters
    ----------
    query : NaturalLanguageQuery
        Natural language query request.

    Returns
    -------
    QueryResponse
        Query execution results with metadata.

    Raises
    ------
    HTTPException
        If query processing or execution fails.

    Examples
    --------
    POST /api/query/nl
    {
        "query": "Show me the top 10 customers by total purchases",
        "visualization_type": "bar",
        "max_results": 10
    }

    Response:
    {
        "success": true,
        "natural_language_query": "Show me the top 10 customers...",
        "generated_sql": "SELECT c.CustomerId, ...",
        "result": {
            "columns": ["CustomerId", "Name", "Total"],
            "rows": [[1, "John Doe", 1234.56], ...],
            "row_count": 10,
            "execution_time_ms": 45.2
        },
        "suggested_visualization": "bar"
    }
    """
    try:
        # Generate SQL from natural language
        generated_sql = nl_to_sql_service.generate_sql(
            query.query, max_results=query.max_results
        )

        # Execute the SQL query
        execution_result = query_executor.execute(
            generated_sql, max_results=query.max_results
        )

        # Create result object
        result = QueryResult(
            columns=execution_result["columns"],
            rows=execution_result["rows"],
            row_count=execution_result["row_count"],
            execution_time_ms=execution_result["execution_time_ms"],
        )

        # Suggest visualization type
        suggested_viz = query.visualization_type or nl_to_sql_service.suggest_visualization(
            generated_sql, execution_result["columns"]
        )

        return QueryResponse(
            success=True,
            natural_language_query=query.query,
            generated_sql=generated_sql,
            result=result,
            suggested_visualization=suggested_viz,
            metadata={
                "executed_at": execution_result["executed_at"],
                "max_results": query.max_results,
            },
        )

    except ValueError as e:
        # SQL generation or validation error
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # General execution error
        raise HTTPException(
            status_code=500, detail=f"Query execution failed: {str(e)}"
        )


@router.post("/sql", response_model=QueryResponse)
async def execute_sql_query(request: QueryRequest):
    """
    Execute a direct SQL query.

    This endpoint allows execution of direct SQL queries without
    natural language processing.

    Parameters
    ----------
    request : QueryRequest
        Query request with SQL or natural language.

    Returns
    -------
    QueryResponse
        Query execution results.

    Raises
    ------
    HTTPException
        If query execution fails.

    Examples
    --------
    POST /api/query/sql
    {
        "sql_query": "SELECT * FROM customers WHERE Country = 'USA' LIMIT 10",
        "max_results": 10
    }
    """
    try:
        # Use provided SQL or generate from natural language
        if request.sql_query:
            sql_query = request.sql_query
            nl_query = request.natural_language_query
        elif request.natural_language_query:
            sql_query = nl_to_sql_service.generate_sql(
                request.natural_language_query, max_results=request.max_results
            )
            nl_query = request.natural_language_query
        else:
            raise HTTPException(
                status_code=400,
                detail="Either sql_query or natural_language_query must be provided",
            )

        # Execute query
        execution_result = query_executor.execute_with_validation(
            sql_query, max_results=request.max_results
        )

        # Create result object
        result = QueryResult(
            columns=execution_result["columns"],
            rows=execution_result["rows"],
            row_count=execution_result["row_count"],
            execution_time_ms=execution_result["execution_time_ms"],
        )

        # Suggest visualization
        suggested_viz = request.visualization_type or nl_to_sql_service.suggest_visualization(
            sql_query, execution_result["columns"]
        )

        return QueryResponse(
            success=True,
            natural_language_query=nl_query,
            generated_sql=sql_query,
            result=result,
            suggested_visualization=suggested_viz,
            metadata={"executed_at": execution_result["executed_at"]},
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Query execution failed: {str(e)}"
        )


@router.post("/explain")
async def explain_query(sql_query: str):
    """
    Generate natural language explanation of SQL query.

    Parameters
    ----------
    sql_query : str
        SQL query to explain.

    Returns
    -------
    dict
        Explanation and query plan.

    Examples
    --------
    POST /api/query/explain
    {
        "sql_query": "SELECT * FROM customers WHERE Country = 'USA'"
    }
    """
    try:
        explanation = nl_to_sql_service.explain_query(sql_query)
        query_plan = query_executor.explain_query_plan(sql_query)

        return {
            "success": True,
            "sql_query": sql_query,
            "explanation": explanation,
            "query_plan": query_plan,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/csv")
async def export_to_csv(request: QueryRequest):
    """
    Execute query and export results as CSV.

    Parameters
    ----------
    request : QueryRequest
        Query request.

    Returns
    -------
    StreamingResponse
        CSV file download.

    Examples
    --------
    POST /api/query/export/csv
    {
        "natural_language_query": "Show all customers"
    }
    """
    try:
        # Generate and execute query
        if request.sql_query:
            sql_query = request.sql_query
        elif request.natural_language_query:
            sql_query = nl_to_sql_service.generate_sql(
                request.natural_language_query
            )
        else:
            raise HTTPException(status_code=400, detail="Query is required")

        result = query_executor.execute_with_validation(sql_query)

        # Format as CSV
        csv_data = query_executor.format_results_as_csv(result)

        # Return as streaming response
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=query_results.csv"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/json")
async def export_to_json(request: QueryRequest):
    """
    Execute query and export results as JSON.

    Parameters
    ----------
    request : QueryRequest
        Query request.

    Returns
    -------
    dict
        JSON formatted results.

    Examples
    --------
    POST /api/query/export/json
    {
        "natural_language_query": "Show all customers"
    }
    """
    try:
        # Generate and execute query
        if request.sql_query:
            sql_query = request.sql_query
        elif request.natural_language_query:
            sql_query = nl_to_sql_service.generate_sql(
                request.natural_language_query
            )
        else:
            raise HTTPException(status_code=400, detail="Query is required")

        result = query_executor.execute_with_validation(sql_query)

        # Format as JSON
        json_data = query_executor.format_results_as_json(result)

        return {
            "success": True,
            "data": json_data,
            "row_count": len(json_data),
            "sql_query": sql_query,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns
    -------
    dict
        Service health status.

    Examples
    --------
    GET /api/query/health
    """
    return {
        "status": "healthy",
        "service": "query",
        "version": settings.api_version,
    }
