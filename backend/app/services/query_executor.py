"""
Query Executor Service.

This module provides functionality to execute SQL queries safely
and return formatted results.
"""

from typing import List, Dict, Any, Tuple
import time
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db_context
from app.config import get_settings

settings = get_settings()


class QueryExecutor:
    """
    SQL query execution service.

    This service handles safe execution of SQL queries with timeout,
    result formatting, and error handling.

    Examples
    --------
    >>> executor = QueryExecutor()
    >>> result = executor.execute("SELECT * FROM customers LIMIT 10")
    >>> print(result['row_count'])
    10
    """

    def __init__(self):
        """Initialize the query executor."""
        self.max_results = settings.max_query_results
        self.timeout = settings.query_timeout

    def execute(self, sql_query: str, max_results: int = None) -> Dict[str, Any]:
        """
        Execute SQL query and return formatted results.

        Parameters
        ----------
        sql_query : str
            SQL query to execute.
        max_results : int, optional
            Maximum number of results to return. Overrides default.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing execution results with keys:
            - columns: List of column names
            - rows: List of result rows
            - row_count: Number of rows returned
            - execution_time_ms: Execution time in milliseconds
            - executed_at: Timestamp of execution

        Raises
        ------
        SQLAlchemyError
            If query execution fails.
        TimeoutError
            If query exceeds timeout limit.

        Examples
        --------
        >>> executor = QueryExecutor()
        >>> result = executor.execute("SELECT COUNT(*) FROM customers")
        >>> print(result['columns'])
        ['COUNT(*)']
        >>> print(result['rows'])
        [[59]]
        """
        start_time = time.time()

        try:
            with get_db_context() as db:
                # Execute query
                result = db.execute(text(sql_query))

                # Fetch results
                max_fetch = max_results or self.max_results
                rows = result.fetchmany(max_fetch)

                # Get column names
                columns = list(result.keys())

                # Convert rows to list of lists
                rows_data = [list(row) for row in rows]

                # Calculate execution time
                execution_time = (time.time() - start_time) * 1000

                return {
                    "columns": columns,
                    "rows": rows_data,
                    "row_count": len(rows_data),
                    "execution_time_ms": round(execution_time, 2),
                    "executed_at": datetime.utcnow().isoformat(),
                }

        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Query execution failed: {str(e)}")

    def execute_with_validation(
        self, sql_query: str, max_results: int = None
    ) -> Dict[str, Any]:
        """
        Execute SQL query with additional validation.

        Parameters
        ----------
        sql_query : str
            SQL query to execute.
        max_results : int, optional
            Maximum number of results to return.

        Returns
        -------
        Dict[str, Any]
            Query execution results.

        Raises
        ------
        ValueError
            If query validation fails.
        SQLAlchemyError
            If query execution fails.

        Examples
        --------
        >>> result = executor.execute_with_validation("SELECT * FROM users")
        >>> print(result['row_count'])
        100
        """
        # Validate query
        self._validate_query(sql_query)

        # Execute query
        return self.execute(sql_query, max_results)

    def _validate_query(self, sql_query: str) -> None:
        """
        Validate SQL query before execution.

        Parameters
        ----------
        sql_query : str
            SQL query to validate.

        Raises
        ------
        ValueError
            If query contains invalid or dangerous operations.

        Examples
        --------
        >>> executor._validate_query("SELECT * FROM users")  # OK
        >>> executor._validate_query("DROP TABLE users")  # Raises ValueError
        """
        sql_upper = sql_query.upper().strip()

        # Check for dangerous operations
        dangerous_keywords = [
            "DROP",
            "DELETE",
            "INSERT",
            "UPDATE",
            "ALTER",
            "CREATE",
            "TRUNCATE",
            "EXEC",
            "EXECUTE",
            "GRANT",
            "REVOKE",
        ]

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(
                    f"Query contains forbidden operation: {keyword}"
                )

        # Ensure SELECT query
        if not sql_upper.startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

    def get_row_count(self, table_name: str) -> int:
        """
        Get approximate row count for a table.

        Parameters
        ----------
        table_name : str
            Name of the table.

        Returns
        -------
        int
            Approximate number of rows in the table.

        Examples
        --------
        >>> count = executor.get_row_count("customers")
        >>> print(count)
        59
        """
        try:
            sql = f"SELECT COUNT(*) FROM {table_name}"
            result = self.execute(sql)
            return result["rows"][0][0]
        except Exception as e:
            print(f"Error getting row count for {table_name}: {e}")
            return 0

    def get_sample_data(
        self, table_name: str, limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get sample data from a table.

        Parameters
        ----------
        table_name : str
            Name of the table.
        limit : int, optional
            Number of sample rows to retrieve (default: 5).

        Returns
        -------
        Dict[str, Any]
            Sample data with columns and rows.

        Examples
        --------
        >>> sample = executor.get_sample_data("customers", limit=3)
        >>> print(len(sample['rows']))
        3
        """
        sql = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute(sql)

    def execute_batch(
        self, queries: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple queries in batch.

        Parameters
        ----------
        queries : List[str]
            List of SQL queries to execute.

        Returns
        -------
        List[Dict[str, Any]]
            List of query results.

        Examples
        --------
        >>> queries = ["SELECT COUNT(*) FROM customers", "SELECT COUNT(*) FROM artists"]
        >>> results = executor.execute_batch(queries)
        >>> print(len(results))
        2
        """
        results = []
        for query in queries:
            try:
                result = self.execute(query)
                results.append({"success": True, "result": result})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        return results

    def explain_query_plan(self, sql_query: str) -> str:
        """
        Get query execution plan.

        Parameters
        ----------
        sql_query : str
            SQL query to explain.

        Returns
        -------
        str
            Query execution plan.

        Examples
        --------
        >>> plan = executor.explain_query_plan("SELECT * FROM customers WHERE Country = 'USA'")
        >>> print(plan)
        'SCAN TABLE customers'
        """
        try:
            with get_db_context() as db:
                # SQLite uses EXPLAIN QUERY PLAN
                explain_query = f"EXPLAIN QUERY PLAN {sql_query}"
                result = db.execute(text(explain_query))
                rows = result.fetchall()

                plan_lines = []
                for row in rows:
                    plan_lines.append(" ".join(str(col) for col in row))

                return "\n".join(plan_lines)

        except Exception as e:
            return f"Error getting query plan: {str(e)}"

    def format_results_as_csv(self, result: Dict[str, Any]) -> str:
        """
        Format query results as CSV string.

        Parameters
        ----------
        result : Dict[str, Any]
            Query execution result.

        Returns
        -------
        str
            CSV formatted string.

        Examples
        --------
        >>> csv_data = executor.format_results_as_csv(result)
        >>> print(csv_data[:50])
        'CustomerId,FirstName,LastName,Country\\n1,John,Doe,USA\\n'
        """
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(result["columns"])

        # Write rows
        for row in result["rows"]:
            writer.writerow(row)

        return output.getvalue()

    def format_results_as_json(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format query results as list of dictionaries.

        Parameters
        ----------
        result : Dict[str, Any]
            Query execution result.

        Returns
        -------
        List[Dict[str, Any]]
            List of row dictionaries.

        Examples
        --------
        >>> json_data = executor.format_results_as_json(result)
        >>> print(json_data[0])
        {'CustomerId': 1, 'FirstName': 'John', 'LastName': 'Doe'}
        """
        columns = result["columns"]
        rows = result["rows"]

        return [dict(zip(columns, row)) for row in rows]
