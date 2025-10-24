"""
Schema Router.

This module defines API endpoints for retrieving database schema information,
query suggestions, and schema analysis.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.models.schema import SchemaResponse, TableSchema, DatabaseSchema
from app.services import SchemaAnalyzer
from app.config import get_settings

router = APIRouter(prefix="/api/schema", tags=["schema"])
settings = get_settings()

# Initialize service
schema_analyzer = SchemaAnalyzer()


@router.get("", response_model=SchemaResponse)
async def get_database_schema():
    """
    Get complete database schema information.

    Returns detailed information about all tables, columns, relationships,
    and constraints in the database.

    Returns
    -------
    SchemaResponse
        Complete database schema with table and relationship information.

    Examples
    --------
    GET /api/schema

    Response:
    {
        "success": true,
        "schema": {
            "tables": [...],
            "table_count": 11,
            "relationships": [...],
            "database_type": "sqlite"
        }
    }
    """
    try:
        formatted_schema = schema_analyzer.get_formatted_schema()

        return SchemaResponse(
            success=True,
            schema=DatabaseSchema(**formatted_schema),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve schema: {str(e)}"
        )


@router.get("/tables")
async def get_table_list():
    """
    Get list of all table names in the database.

    Returns
    -------
    dict
        List of table names.

    Examples
    --------
    GET /api/schema/tables

    Response:
    {
        "success": true,
        "tables": ["albums", "artists", "customers", ...],
        "count": 11
    }
    """
    try:
        schema = schema_analyzer.get_formatted_schema()
        table_names = [table["name"] for table in schema["tables"]]

        return {
            "success": True,
            "tables": table_names,
            "count": len(table_names),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables/{table_name}")
async def get_table_schema(table_name: str):
    """
    Get detailed schema information for a specific table.

    Parameters
    ----------
    table_name : str
        Name of the table.

    Returns
    -------
    dict
        Table schema details including columns, keys, and statistics.

    Examples
    --------
    GET /api/schema/tables/customers

    Response:
    {
        "success": true,
        "table": {
            "name": "customers",
            "columns": [...],
            "primary_keys": ["CustomerId"],
            "foreign_keys": [],
            "row_count": 59
        }
    }
    """
    try:
        schema = schema_analyzer.get_formatted_schema()
        table = next(
            (t for t in schema["tables"] if t["name"] == table_name), None
        )

        if not table:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        return {
            "success": True,
            "table": table,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables/{table_name}/related")
async def get_related_tables(table_name: str):
    """
    Get tables related to the specified table through foreign keys.

    Parameters
    ----------
    table_name : str
        Name of the table.

    Returns
    -------
    dict
        List of related tables with relationship information.

    Examples
    --------
    GET /api/schema/tables/invoices/related

    Response:
    {
        "success": true,
        "table": "invoices",
        "related_tables": [
            {
                "table": "customers",
                "relationship_type": "many_to_one",
                "foreign_key_column": "CustomerId"
            }
        ]
    }
    """
    try:
        related = schema_analyzer.find_related_tables(table_name)

        return {
            "success": True,
            "table": table_name,
            "related_tables": related,
            "count": len(related),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables/{table_name}/statistics")
async def get_table_statistics(table_name: str):
    """
    Get statistical information about a table.

    Parameters
    ----------
    table_name : str
        Name of the table.

    Returns
    -------
    dict
        Table statistics including row count, column count, and sample data.

    Examples
    --------
    GET /api/schema/tables/customers/statistics

    Response:
    {
        "success": true,
        "statistics": {
            "table_name": "customers",
            "row_count": 59,
            "column_count": 13,
            "sample_data": {...}
        }
    }
    """
    try:
        stats = schema_analyzer.get_table_statistics(table_name)

        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])

        return {
            "success": True,
            "statistics": stats,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions")
async def get_query_suggestions():
    """
    Get intelligent query suggestions based on database schema.

    Returns suggested queries categorized by complexity and type,
    helping users explore the database.

    Returns
    -------
    dict
        List of query suggestions with categories and descriptions.

    Examples
    --------
    GET /api/schema/suggestions

    Response:
    {
        "success": true,
        "suggestions": [
            {
                "category": "Basic Queries",
                "query": "Show all customers",
                "description": "Retrieve all records from customers table",
                "difficulty": "easy"
            },
            ...
        ],
        "count": 15
    }
    """
    try:
        suggestions = schema_analyzer.get_query_suggestions()

        return {
            "success": True,
            "suggestions": suggestions,
            "count": len(suggestions),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_schema(
    q: str = Query(..., description="Search term for columns", min_length=1)
):
    """
    Search for columns matching a search term.

    Parameters
    ----------
    q : str
        Search term to find in column names.

    Returns
    -------
    dict
        List of matching columns with table information.

    Examples
    --------
    GET /api/schema/search?q=name

    Response:
    {
        "success": true,
        "results": [
            {
                "table": "customers",
                "column": "FirstName",
                "type": "NVARCHAR(40)",
                "nullable": true
            },
            ...
        ],
        "count": 5
    }
    """
    try:
        results = schema_analyzer.search_columns(q)

        return {
            "success": True,
            "query": q,
            "results": results,
            "count": len(results),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/relationships")
async def get_relationships():
    """
    Get all foreign key relationships in the database.

    Returns
    -------
    dict
        List of all relationships between tables.

    Examples
    --------
    GET /api/schema/relationships

    Response:
    {
        "success": true,
        "relationships": [
            {
                "from_table": "invoices",
                "from_column": ["CustomerId"],
                "to_table": "customers",
                "to_column": ["CustomerId"]
            },
            ...
        ],
        "count": 10
    }
    """
    try:
        schema = schema_analyzer.get_formatted_schema()
        relationships = schema.get("relationships", [])

        return {
            "success": True,
            "relationships": relationships,
            "count": len(relationships),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/erd")
async def get_erd_data():
    """
    Get Entity Relationship Diagram data for visualization.

    Returns data structure suitable for rendering ERD diagrams in the frontend.

    Returns
    -------
    dict
        ERD data with nodes (tables) and edges (relationships).

    Examples
    --------
    GET /api/schema/erd

    Response:
    {
        "success": true,
        "erd": {
            "nodes": [...],
            "edges": [...],
            "layout": "hierarchical"
        }
    }
    """
    try:
        erd_data = schema_analyzer.generate_erd_data()

        return {
            "success": True,
            "erd": erd_data,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Health check endpoint for schema service.

    Returns
    -------
    dict
        Service health status.

    Examples
    --------
    GET /api/schema/health
    """
    return {
        "status": "healthy",
        "service": "schema",
        "version": settings.api_version,
    }
