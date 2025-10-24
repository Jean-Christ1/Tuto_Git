"""
Database Module.

This module handles database connections, session management, and provides
utility functions for database operations.
"""

from typing import Generator
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager

from app.config import get_settings

settings = get_settings()

# Create SQLAlchemy engine
if settings.database_url.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.database_echo,
    )
else:
    # Other databases (PostgreSQL, MySQL, etc.)
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        echo=settings.database_echo,
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Metadata for reflection
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.

    Provides a database session for dependency injection in FastAPI routes.
    The session is automatically closed after the request is completed.

    Yields
    ------
    Session
        SQLAlchemy database session.

    Examples
    --------
    >>> from fastapi import Depends
    >>> @app.get("/items")
    >>> def read_items(db: Session = Depends(get_db)):
    >>>     return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Get database session context manager.

    Provides a database session as a context manager for use outside
    of FastAPI dependency injection.

    Yields
    ------
    Session
        SQLAlchemy database session.

    Examples
    --------
    >>> with get_db_context() as db:
    >>>     items = db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_table_names() -> list:
    """
    Get list of all table names in the database.

    Returns
    -------
    list
        List of table name strings.

    Examples
    --------
    >>> tables = get_table_names()
    >>> print(tables)
    ['albums', 'artists', 'customers', ...]
    """
    inspector = inspect(engine)
    return inspector.get_table_names()


def get_table_schema(table_name: str) -> dict:
    """
    Get schema information for a specific table.

    Parameters
    ----------
    table_name : str
        Name of the table to inspect.

    Returns
    -------
    dict
        Dictionary containing table schema information including columns,
        types, and constraints.

    Examples
    --------
    >>> schema = get_table_schema('customers')
    >>> print(schema['columns'])
    [{'name': 'CustomerId', 'type': 'INTEGER', ...}, ...]
    """
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    pk_constraint = inspector.get_pk_constraint(table_name)
    foreign_keys = inspector.get_foreign_keys(table_name)
    indexes = inspector.get_indexes(table_name)

    return {
        "table_name": table_name,
        "columns": columns,
        "primary_key": pk_constraint,
        "foreign_keys": foreign_keys,
        "indexes": indexes,
    }


def get_database_schema() -> dict:
    """
    Get complete database schema information.

    Returns
    -------
    dict
        Dictionary containing schema information for all tables in the database.

    Examples
    --------
    >>> schema = get_database_schema()
    >>> print(schema.keys())
    dict_keys(['tables', 'table_count', 'relationships'])
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    tables = {}
    for table_name in table_names:
        tables[table_name] = get_table_schema(table_name)

    # Build relationships map
    relationships = []
    for table_name, table_info in tables.items():
        for fk in table_info["foreign_keys"]:
            relationships.append(
                {
                    "from_table": table_name,
                    "from_column": fk["constrained_columns"],
                    "to_table": fk["referred_table"],
                    "to_column": fk["referred_columns"],
                }
            )

    return {
        "tables": tables,
        "table_count": len(tables),
        "relationships": relationships,
    }


def test_connection() -> bool:
    """
    Test database connection.

    Returns
    -------
    bool
        True if connection successful, False otherwise.

    Examples
    --------
    >>> is_connected = test_connection()
    >>> print(f"Database connected: {is_connected}")
    Database connected: True
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def close_db_connection():
    """
    Close database connection and dispose of the engine.

    This function should be called when shutting down the application
    to ensure all connections are properly closed.

    Examples
    --------
    >>> close_db_connection()
    """
    engine.dispose()
