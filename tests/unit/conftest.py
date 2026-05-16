"""
Shared pytest fixtures for unit tests.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_duckdb_path(tmp_path):
    """
    Provides a temporary DuckDB file path for testing.

    Returns:
        Path: Path to a temporary .duckdb file
    """
    db_path = tmp_path / "test_pipeline.duckdb"
    return str(db_path)


@pytest.fixture
def mock_notion_credentials():
    """
    Provides mock Notion API credentials for testing.

    Returns:
        dict: Mock credentials dictionary
    """
    return {"api_key": "test_api_key_mock_value"}
