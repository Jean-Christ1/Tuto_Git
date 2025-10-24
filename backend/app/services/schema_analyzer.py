"""
Schema Analyzer Service.

This module provides functionality to analyze database schema,
generate documentation, and provide intelligent query suggestions.
"""

from typing import List, Dict, Any, Optional
from collections import defaultdict

from app.database import get_database_schema, get_table_schema
from app.services.query_executor import QueryExecutor


class SchemaAnalyzer:
    """
    Database schema analysis service.

    This service analyzes database schema to provide insights,
    documentation, and intelligent query suggestions.

    Attributes
    ----------
    schema : dict
        Complete database schema information.
    executor : QueryExecutor
        Query executor for getting table statistics.

    Examples
    --------
    >>> analyzer = SchemaAnalyzer()
    >>> suggestions = analyzer.get_query_suggestions()
    >>> print(len(suggestions))
    15
    """

    def __init__(self):
        """Initialize the schema analyzer."""
        self.schema = get_database_schema()
        self.executor = QueryExecutor()

    def get_formatted_schema(self) -> Dict[str, Any]:
        """
        Get formatted schema information for API responses.

        Returns
        -------
        Dict[str, Any]
            Formatted schema information with table details,
            relationships, and statistics.

        Examples
        --------
        >>> schema = analyzer.get_formatted_schema()
        >>> print(schema['table_count'])
        11
        >>> print(schema['tables'][0]['name'])
        'albums'
        """
        formatted_tables = []

        for table_name, table_info in self.schema["tables"].items():
            # Format columns
            columns = []
            for col in table_info["columns"]:
                column_info = {
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col.get("nullable", True),
                    "default": col.get("default"),
                    "primary_key": False,
                    "foreign_key": None,
                }

                # Check if primary key
                pk_cols = table_info.get("primary_key", {}).get(
                    "constrained_columns", []
                )
                if col["name"] in pk_cols:
                    column_info["primary_key"] = True

                # Check if foreign key
                for fk in table_info.get("foreign_keys", []):
                    if col["name"] in fk.get("constrained_columns", []):
                        column_info["foreign_key"] = {
                            "table": fk.get("referred_table"),
                            "column": fk.get("referred_columns", [])[0]
                            if fk.get("referred_columns")
                            else None,
                        }

                columns.append(column_info)

            # Get row count
            try:
                row_count = self.executor.get_row_count(table_name)
            except:
                row_count = None

            formatted_table = {
                "name": table_name,
                "columns": columns,
                "primary_keys": table_info.get("primary_key", {}).get(
                    "constrained_columns", []
                ),
                "foreign_keys": table_info.get("foreign_keys", []),
                "row_count": row_count,
                "description": self._generate_table_description(table_name, columns),
            }

            formatted_tables.append(formatted_table)

        return {
            "tables": formatted_tables,
            "table_count": len(formatted_tables),
            "relationships": self.schema.get("relationships", []),
            "database_type": "sqlite",  # Can be made dynamic
        }

    def _generate_table_description(
        self, table_name: str, columns: List[Dict[str, Any]]
    ) -> str:
        """
        Generate human-readable description for a table.

        Parameters
        ----------
        table_name : str
            Name of the table.
        columns : List[Dict[str, Any]]
            List of column information.

        Returns
        -------
        str
            Human-readable table description.

        Examples
        --------
        >>> desc = analyzer._generate_table_description("customers", columns)
        >>> print(desc)
        'Stores customer information including contact details and location'
        """
        # Common table descriptions (can be expanded)
        descriptions = {
            "customers": "Stores customer information including contact details and location",
            "invoices": "Contains invoice records with billing information and totals",
            "invoice_items": "Stores individual line items for each invoice",
            "tracks": "Music track information including name, composer, and duration",
            "albums": "Album information with titles and related artists",
            "artists": "Artist information and names",
            "genres": "Music genre classifications",
            "media_types": "Types of media formats for tracks",
            "playlists": "Playlist collections of tracks",
            "playlist_track": "Mapping table linking playlists to tracks",
            "employees": "Employee information including titles and reporting structure",
        }

        return descriptions.get(
            table_name.lower(),
            f"Contains {table_name} data with {len(columns)} columns",
        )

    def get_query_suggestions(self) -> List[Dict[str, str]]:
        """
        Generate intelligent query suggestions based on schema.

        Returns
        -------
        List[Dict[str, str]]
            List of suggested queries with categories.

        Examples
        --------
        >>> suggestions = analyzer.get_query_suggestions()
        >>> print(suggestions[0])
        {'category': 'Basic Queries', 'query': 'Show all customers', 'description': '...'}
        """
        suggestions = []

        # Basic queries for each table
        for table_name in list(self.schema["tables"].keys())[:5]:
            suggestions.append(
                {
                    "category": "Basic Queries",
                    "query": f"Show all {table_name}",
                    "description": f"Retrieve all records from {table_name} table",
                    "difficulty": "easy",
                }
            )

        # Aggregate queries
        aggregate_suggestions = [
            {
                "category": "Analytics",
                "query": "What are the total sales by country?",
                "description": "Aggregate invoice totals grouped by country",
                "difficulty": "medium",
            },
            {
                "category": "Analytics",
                "query": "Show the top 10 best-selling tracks",
                "description": "Find most frequently purchased tracks",
                "difficulty": "medium",
            },
            {
                "category": "Analytics",
                "query": "What is the average invoice amount?",
                "description": "Calculate average value of all invoices",
                "difficulty": "easy",
            },
            {
                "category": "Analytics",
                "query": "How many customers are there in each country?",
                "description": "Count customers grouped by country",
                "difficulty": "easy",
            },
        ]
        suggestions.extend(aggregate_suggestions)

        # Join queries
        join_suggestions = [
            {
                "category": "Complex Queries",
                "query": "List all tracks with their album and artist names",
                "description": "Join tracks, albums, and artists tables",
                "difficulty": "hard",
            },
            {
                "category": "Complex Queries",
                "query": "Show customer purchase history with invoice details",
                "description": "Join customers with invoices and line items",
                "difficulty": "hard",
            },
            {
                "category": "Complex Queries",
                "query": "Which genres generate the most revenue?",
                "description": "Join multiple tables and aggregate by genre",
                "difficulty": "hard",
            },
        ]
        suggestions.extend(join_suggestions)

        # Time-based queries
        time_suggestions = [
            {
                "category": "Time Series",
                "query": "Show sales trends by month",
                "description": "Group sales by month to see trends",
                "difficulty": "medium",
            },
            {
                "category": "Time Series",
                "query": "What were the total sales in 2023?",
                "description": "Filter and sum invoices for specific year",
                "difficulty": "easy",
            },
        ]
        suggestions.extend(time_suggestions)

        return suggestions

    def find_related_tables(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Find tables related to a given table through foreign keys.

        Parameters
        ----------
        table_name : str
            Name of the table to find relationships for.

        Returns
        -------
        List[Dict[str, Any]]
            List of related tables with relationship information.

        Examples
        --------
        >>> related = analyzer.find_related_tables("invoices")
        >>> print(related[0]['table'])
        'customers'
        >>> print(related[0]['relationship_type'])
        'many_to_one'
        """
        related = []

        # Tables this table references (many-to-one)
        table_info = self.schema["tables"].get(table_name, {})
        for fk in table_info.get("foreign_keys", []):
            related.append(
                {
                    "table": fk["referred_table"],
                    "relationship_type": "many_to_one",
                    "foreign_key_column": fk["constrained_columns"][0]
                    if fk["constrained_columns"]
                    else None,
                    "referenced_column": fk["referred_columns"][0]
                    if fk["referred_columns"]
                    else None,
                }
            )

        # Tables that reference this table (one-to-many)
        for other_table_name, other_table_info in self.schema["tables"].items():
            if other_table_name == table_name:
                continue

            for fk in other_table_info.get("foreign_keys", []):
                if fk["referred_table"] == table_name:
                    related.append(
                        {
                            "table": other_table_name,
                            "relationship_type": "one_to_many",
                            "foreign_key_column": fk["constrained_columns"][0]
                            if fk["constrained_columns"]
                            else None,
                            "referenced_column": fk["referred_columns"][0]
                            if fk["referred_columns"]
                            else None,
                        }
                    )

        return related

    def get_table_statistics(self, table_name: str) -> Dict[str, Any]:
        """
        Get detailed statistics for a table.

        Parameters
        ----------
        table_name : str
            Name of the table.

        Returns
        -------
        Dict[str, Any]
            Table statistics including row count, column count, etc.

        Examples
        --------
        >>> stats = analyzer.get_table_statistics("customers")
        >>> print(stats['row_count'])
        59
        """
        try:
            row_count = self.executor.get_row_count(table_name)
            sample_data = self.executor.get_sample_data(table_name, limit=5)

            table_info = self.schema["tables"].get(table_name, {})

            return {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(table_info.get("columns", [])),
                "has_primary_key": bool(table_info.get("primary_key")),
                "foreign_key_count": len(table_info.get("foreign_keys", [])),
                "sample_data": sample_data,
            }
        except Exception as e:
            return {"error": str(e)}

    def search_columns(self, search_term: str) -> List[Dict[str, str]]:
        """
        Search for columns matching a search term.

        Parameters
        ----------
        search_term : str
            Term to search for in column names.

        Returns
        -------
        List[Dict[str, str]]
            List of matching columns with table information.

        Examples
        --------
        >>> results = analyzer.search_columns("name")
        >>> print(results[0])
        {'table': 'customers', 'column': 'FirstName', 'type': 'NVARCHAR(40)'}
        """
        results = []
        search_lower = search_term.lower()

        for table_name, table_info in self.schema["tables"].items():
            for column in table_info.get("columns", []):
                if search_lower in column["name"].lower():
                    results.append(
                        {
                            "table": table_name,
                            "column": column["name"],
                            "type": str(column["type"]),
                            "nullable": column.get("nullable", True),
                        }
                    )

        return results

    def generate_erd_data(self) -> Dict[str, Any]:
        """
        Generate data for Entity Relationship Diagram visualization.

        Returns
        -------
        Dict[str, Any]
            ERD data with nodes and edges for visualization.

        Examples
        --------
        >>> erd = analyzer.generate_erd_data()
        >>> print(len(erd['nodes']))
        11
        >>> print(len(erd['edges']))
        10
        """
        nodes = []
        edges = []

        # Create nodes for each table
        for table_name, table_info in self.schema["tables"].items():
            node = {
                "id": table_name,
                "label": table_name,
                "columns": [
                    {
                        "name": col["name"],
                        "type": str(col["type"]),
                        "is_pk": col["name"]
                        in table_info.get("primary_key", {}).get(
                            "constrained_columns", []
                        ),
                    }
                    for col in table_info.get("columns", [])
                ],
            }
            nodes.append(node)

        # Create edges for relationships
        for relationship in self.schema.get("relationships", []):
            edge = {
                "from": relationship["from_table"],
                "to": relationship["to_table"],
                "from_column": relationship["from_column"],
                "to_column": relationship["to_column"],
                "type": "many_to_one",
            }
            edges.append(edge)

        return {"nodes": nodes, "edges": edges, "layout": "hierarchical"}
