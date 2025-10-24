"""
Natural Language to SQL Service.

This module provides functionality to convert natural language queries
into SQL statements using LangChain and LLM models.
"""

from typing import Optional, Dict, Any, List
import re
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains import LLMChain

from app.config import get_settings
from app.database import get_database_schema

settings = get_settings()


class NLToSQLService:
    """
    Natural Language to SQL conversion service.

    This service uses LangChain and LLM providers to convert natural
    language queries into valid SQL statements based on the database schema.

    Attributes
    ----------
    llm : ChatOpenAI or ChatAnthropic
        Language model instance for query generation.
    schema : dict
        Database schema information.
    prompt_template : PromptTemplate
        Template for generating SQL from natural language.

    Examples
    --------
    >>> service = NLToSQLService()
    >>> sql = service.generate_sql("Show me all customers from USA")
    >>> print(sql)
    "SELECT * FROM customers WHERE Country = 'USA'"
    """

    def __init__(self):
        """
        Initialize the NL to SQL service.

        Sets up the LLM provider and loads database schema information.
        """
        self.llm = self._initialize_llm()
        self.schema = get_database_schema()
        self.prompt_template = self._create_prompt_template()

    def _initialize_llm(self):
        """
        Initialize the language model based on configuration.

        Returns
        -------
        ChatOpenAI or ChatAnthropic
            Initialized language model instance.

        Raises
        ------
        ValueError
            If API key is not configured or provider is invalid.

        Examples
        --------
        >>> llm = service._initialize_llm()
        >>> print(type(llm).__name__)
        'ChatOpenAI'
        """
        if settings.llm_provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return ChatOpenAI(
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                api_key=settings.openai_api_key,
            )
        elif settings.llm_provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            return ChatAnthropic(
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                api_key=settings.anthropic_api_key,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")

    def _create_prompt_template(self) -> PromptTemplate:
        """
        Create prompt template for SQL generation.

        Returns
        -------
        PromptTemplate
            LangChain prompt template for SQL generation.

        Examples
        --------
        >>> template = service._create_prompt_template()
        >>> print(template.template[:50])
        'You are a SQL expert. Convert the following natura...'
        """
        schema_description = self._format_schema_for_prompt()

        template = """You are a SQL expert. Convert the following natural language query into a valid SQL statement.

Database Schema:
{schema}

Rules:
1. Generate only the SQL query without any explanation
2. Use proper SQL syntax for the database type
3. Include appropriate JOINs when querying multiple tables
4. Use proper column names exactly as shown in the schema
5. Add LIMIT clause if not specified (default: 100)
6. Use aggregate functions (COUNT, SUM, AVG, etc.) when appropriate
7. Handle NULL values appropriately
8. Use proper date/time functions if needed
9. Return only SELECT queries (no INSERT, UPDATE, DELETE)
10. Ensure the query is safe and doesn't expose sensitive operations

Natural Language Query: {query}

SQL Query:"""

        return PromptTemplate(
            input_variables=["schema", "query"],
            template=template,
        )

    def _format_schema_for_prompt(self) -> str:
        """
        Format database schema for inclusion in the prompt.

        Returns
        -------
        str
            Formatted schema description.

        Examples
        --------
        >>> schema_text = service._format_schema_for_prompt()
        >>> print(schema_text[:100])
        'Table: albums\\n  Columns:\\n    - AlbumId (INTEGER, PRIMARY KEY)\\n    - Title...'
        """
        schema_text = []

        for table_name, table_info in self.schema["tables"].items():
            schema_text.append(f"\nTable: {table_name}")
            schema_text.append("  Columns:")

            for column in table_info["columns"]:
                col_desc = f"    - {column['name']} ({column['type']}"
                if column.get("nullable") == False:
                    col_desc += ", NOT NULL"
                if column.get("default"):
                    col_desc += f", DEFAULT {column['default']}"
                col_desc += ")"
                schema_text.append(col_desc)

            # Add primary key info
            if table_info.get("primary_key"):
                pk_cols = table_info["primary_key"].get("constrained_columns", [])
                if pk_cols:
                    schema_text.append(f"  Primary Key: {', '.join(pk_cols)}")

            # Add foreign key info
            if table_info.get("foreign_keys"):
                schema_text.append("  Foreign Keys:")
                for fk in table_info["foreign_keys"]:
                    fk_desc = f"    - {', '.join(fk['constrained_columns'])} -> {fk['referred_table']}.{', '.join(fk['referred_columns'])}"
                    schema_text.append(fk_desc)

        return "\n".join(schema_text)

    def generate_sql(
        self, natural_language_query: str, max_results: Optional[int] = None
    ) -> str:
        """
        Generate SQL query from natural language.

        Parameters
        ----------
        natural_language_query : str
            Natural language query to convert.
        max_results : Optional[int]
            Maximum number of results to return (adds LIMIT clause).

        Returns
        -------
        str
            Generated SQL query.

        Raises
        ------
        ValueError
            If query generation fails or produces invalid SQL.

        Examples
        --------
        >>> sql = service.generate_sql("Show top 5 customers by purchases")
        >>> print(sql)
        'SELECT c.CustomerId, c.FirstName, c.LastName, SUM(i.Total) as TotalPurchases...'
        """
        try:
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

            # Generate SQL
            response = chain.run(
                schema=self._format_schema_for_prompt(), query=natural_language_query
            )

            # Clean up the response
            sql_query = self._clean_sql_response(response)

            # Add LIMIT if specified and not already present
            if max_results and "LIMIT" not in sql_query.upper():
                sql_query = f"{sql_query.rstrip(';')} LIMIT {max_results}"

            # Validate the generated SQL
            self._validate_sql(sql_query)

            return sql_query

        except Exception as e:
            raise ValueError(f"Failed to generate SQL: {str(e)}")

    def _clean_sql_response(self, response: str) -> str:
        """
        Clean and extract SQL query from LLM response.

        Parameters
        ----------
        response : str
            Raw response from LLM.

        Returns
        -------
        str
            Cleaned SQL query.

        Examples
        --------
        >>> sql = service._clean_sql_response("```sql\\nSELECT * FROM users\\n```")
        >>> print(sql)
        'SELECT * FROM users'
        """
        # Remove markdown code blocks
        response = re.sub(r"```sql\s*", "", response)
        response = re.sub(r"```\s*", "", response)

        # Remove common prefixes
        prefixes = ["SQL Query:", "Query:", "SQL:"]
        for prefix in prefixes:
            if response.strip().startswith(prefix):
                response = response.strip()[len(prefix) :].strip()

        # Remove trailing semicolons and whitespace
        response = response.strip().rstrip(";").strip()

        return response

    def _validate_sql(self, sql_query: str) -> None:
        """
        Validate generated SQL query for safety and correctness.

        Parameters
        ----------
        sql_query : str
            SQL query to validate.

        Raises
        ------
        ValueError
            If SQL query is invalid or contains dangerous operations.

        Examples
        --------
        >>> service._validate_sql("SELECT * FROM users")  # OK
        >>> service._validate_sql("DROP TABLE users")  # Raises ValueError
        """
        # Convert to uppercase for checking
        sql_upper = sql_query.upper()

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
        ]

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(
                    f"SQL query contains forbidden operation: {keyword}"
                )

        # Ensure it's a SELECT query
        if not sql_upper.strip().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        # Basic SQL injection prevention
        suspicious_patterns = [
            r";\s*SELECT",
            r";\s*DROP",
            r"--",
            r"/\*",
            r"\*/",
            r"xp_",
            r"sp_",
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, sql_query, re.IGNORECASE):
                raise ValueError("SQL query contains suspicious pattern")

    def suggest_visualization(
        self, sql_query: str, result_columns: List[str]
    ) -> str:
        """
        Suggest appropriate visualization type based on query and results.

        Parameters
        ----------
        sql_query : str
            Generated SQL query.
        result_columns : List[str]
            Column names in the result set.

        Returns
        -------
        str
            Suggested visualization type (bar, line, pie, table, etc.).

        Examples
        --------
        >>> viz = service.suggest_visualization(
        ...     "SELECT Country, COUNT(*) FROM customers GROUP BY Country",
        ...     ["Country", "COUNT(*)"]
        ... )
        >>> print(viz)
        'bar'
        """
        sql_upper = sql_query.upper()
        num_columns = len(result_columns)

        # Time series data
        if any(
            keyword in sql_upper
            for keyword in ["DATE", "MONTH", "YEAR", "TIME", "TIMESTAMP"]
        ):
            return "line"

        # Aggregate functions with grouping
        if "GROUP BY" in sql_upper:
            if num_columns == 2:
                # Single dimension aggregation
                if any(func in sql_upper for func in ["SUM", "COUNT", "AVG"]):
                    # Prefer pie chart for counts/percentages, bar for sums
                    if "COUNT" in sql_upper and "COUNTRY" in sql_upper:
                        return "pie"
                    return "bar"
            elif num_columns > 2:
                # Multi-dimensional data
                return "bar"

        # Large result sets
        if "LIMIT" in sql_upper:
            limit_match = re.search(r"LIMIT\s+(\d+)", sql_upper)
            if limit_match and int(limit_match.group(1)) > 20:
                return "table"

        # Default to table for complex queries
        if num_columns > 4:
            return "table"

        # Simple two-column data
        if num_columns == 2:
            return "bar"

        # Default
        return "table"

    def explain_query(self, sql_query: str) -> str:
        """
        Generate natural language explanation of SQL query.

        Parameters
        ----------
        sql_query : str
            SQL query to explain.

        Returns
        -------
        str
            Natural language explanation of the query.

        Examples
        --------
        >>> explanation = service.explain_query(
        ...     "SELECT * FROM customers WHERE Country = 'USA'"
        ... )
        >>> print(explanation)
        'This query retrieves all customers located in the USA.'
        """
        explain_prompt = PromptTemplate(
            input_variables=["sql_query"],
            template="""Explain the following SQL query in simple, non-technical language:

SQL Query: {sql_query}

Explanation:""",
        )

        chain = LLMChain(llm=self.llm, prompt=explain_prompt)
        explanation = chain.run(sql_query=sql_query)

        return explanation.strip()
