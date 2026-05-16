"""
Tier 1 data tests for Notion bronze tables.

Tests schema integrity: _dlt_id non-null and unique.
Covers all main tables in src_abc_2 schema.
"""

import pytest


class TestTier1SchemaIntegrity:
    """Tier 1: Schema integrity tests for all Notion bronze tables."""

    @pytest.mark.parametrize(
        "table_name",
        [
            "tasks",
            "tasks_tracker",
            "untitled_2e982b21",
        ],
    )
    def test_dlt_id_not_null(self, duckdb_conn, bronze_schema, table_name):
        """
        Test that _dlt_id column has no NULL values.

        This is a Tier 1 mandatory test. The _dlt_id column is the primary
        key assigned by dlt and must never be NULL.

        Args:
            duckdb_conn: DuckDB connection fixture
            bronze_schema: Bronze schema name fixture
            table_name: Table name (parameterized)
        """
        query = f"""
            SELECT COUNT(*) as null_count
            FROM {bronze_schema}.{table_name}
            WHERE _dlt_id IS NULL
        """
        result = duckdb_conn.execute(query).fetchone()
        null_count = result[0]

        assert null_count == 0, (
            f"Found {null_count} NULL values in {bronze_schema}.{table_name}._dlt_id. "
            f"All rows must have a valid _dlt_id."
        )

    @pytest.mark.parametrize(
        "table_name",
        [
            "tasks",
            "tasks_tracker",
            "untitled_2e982b21",
        ],
    )
    def test_dlt_id_unique(self, duckdb_conn, bronze_schema, table_name):
        """
        Test that _dlt_id column has only unique values.

        This is a Tier 1 mandatory test. The _dlt_id must be unique
        within each table to serve as a reliable primary key.

        Args:
            duckdb_conn: DuckDB connection fixture
            bronze_schema: Bronze schema name fixture
            table_name: Table name (parameterized)
        """
        query = f"""
            SELECT COUNT(*) as total_count,
                   COUNT(DISTINCT _dlt_id) as unique_count
            FROM {bronze_schema}.{table_name}
        """
        result = duckdb_conn.execute(query).fetchone()
        total_count, unique_count = result

        assert total_count == unique_count, (
            f"Duplicate _dlt_id values found in {bronze_schema}.{table_name}. "
            f"Total rows: {total_count}, Unique _dlt_id: {unique_count}, "
            f"Duplicates: {total_count - unique_count}"
        )

    @pytest.mark.parametrize(
        "table_name",
        [
            "tasks",
            "tasks_tracker",
            "untitled_2e982b21",
        ],
    )
    def test_table_not_empty(self, duckdb_conn, bronze_schema, table_name):
        """
        Test that bronze tables contain data.

        While not strictly Tier 1, this is a basic sanity check that
        the pipeline actually loaded data.

        Args:
            duckdb_conn: DuckDB connection fixture
            bronze_schema: Bronze schema name fixture
            table_name: Table name (parameterized)
        """
        query = f"""
            SELECT COUNT(*) as row_count
            FROM {bronze_schema}.{table_name}
        """
        result = duckdb_conn.execute(query).fetchone()
        row_count = result[0]

        assert row_count > 0, (
            f"Table {bronze_schema}.{table_name} is empty. "
            f"Expected at least 1 row from Notion."
        )
