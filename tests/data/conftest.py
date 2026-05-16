"""
Shared fixtures for data tests.

Provides DuckDB connection to bronze tables.
"""

import pytest
import duckdb
from pathlib import Path


@pytest.fixture(scope="session")
def duckdb_conn():
    """
    Provides a read-only connection to the bronze DuckDB database.

    Returns:
        duckdb.DuckDBPyConnection: Connection to ./data/prod.duckdb
    """
    db_path = Path("./data/prod.duckdb")
    if not db_path.exists():
        pytest.skip(f"Database not found at {db_path}")

    conn = duckdb.connect(str(db_path), read_only=True)
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def bronze_schema():
    """
    Returns the bronze schema name for Notion data.

    Returns:
        str: Schema name (src_abc_2)
    """
    return "src_abc_2"
