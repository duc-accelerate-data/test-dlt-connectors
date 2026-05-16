"""
Unit tests for Notion ingestion pipeline.

Tests the abc_2_bronze pipeline using mocked Notion API responses.
Does not make live API calls.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import importlib.util
from pathlib import Path


class TestNotionPipeline:
    """Test suite for Notion database ingestion pipeline."""

    @pytest.fixture
    def pipeline_module(self):
        """Load the pipeline module from file."""
        pipeline_path = Path("dlt/pipeline.py")
        spec = importlib.util.spec_from_file_location("pipeline_module", pipeline_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["pipeline_module"] = module
        spec.loader.exec_module(module)
        return module

    def test_pipeline_file_exists(self):
        """Verify pipeline file exists and is readable."""
        pipeline_path = Path("dlt/pipeline.py")
        assert pipeline_path.exists()
        assert pipeline_path.is_file()

    def test_pipeline_has_run_function(self, pipeline_module):
        """Verify pipeline module has run() function."""
        assert hasattr(pipeline_module, "run")
        assert callable(pipeline_module.run)

    def test_pipeline_has_documentation(self, pipeline_module):
        """Verify pipeline module and run() have docstrings."""
        assert pipeline_module.__doc__ is not None
        assert "Notion" in pipeline_module.__doc__
        assert pipeline_module.run.__doc__ is not None

    def test_pipeline_source_code_contains_abc_2(self, pipeline_module):
        """
        Test that pipeline source code references abc_2 connection.

        Verifies:
        - Source code contains section="abc_2" configuration
        """
        import inspect

        source_code = inspect.getsource(pipeline_module.run)
        assert 'section="abc_2"' in source_code or "section='abc_2'" in source_code

    @patch("notion.notion_databases")
    def test_pipeline_configuration_parameters(self, mock_notion_databases, pipeline_module):
        """
        Test pipeline is configured with correct parameters.

        Verifies:
        - Pipeline name: abc_2_bronze
        - Dataset name: src_abc_2
        - Destination: DuckDB
        """
        # Setup mocks
        mock_source = MagicMock()
        mock_notion_databases.with_args.return_value.return_value = mock_source

        with patch("dlt.pipeline") as mock_dlt_pipeline:
            mock_pipeline_instance = MagicMock()
            mock_dlt_pipeline.return_value = mock_pipeline_instance
            mock_pipeline_instance.run.return_value = MagicMock(has_failed_jobs=False)

            # Run pipeline
            pipeline_module.run()

            # Verify pipeline creation
            mock_dlt_pipeline.assert_called_once()
            call_kwargs = mock_dlt_pipeline.call_args.kwargs

            assert call_kwargs["pipeline_name"] == "abc_2_bronze"
            assert call_kwargs["dataset_name"] == "src_abc_2"
            # Destination should be configured (duckdb object)
            assert "destination" in call_kwargs

    @patch("notion.notion_databases")
    def test_pipeline_returns_load_info(self, mock_notion_databases, pipeline_module):
        """
        Test that pipeline returns load_info object.

        Verifies:
        - run() returns a value (load_info)
        - Returned value has expected structure
        """
        # Setup mocks
        mock_source = MagicMock()
        mock_notion_databases.with_args.return_value.return_value = mock_source

        with patch("dlt.pipeline") as mock_dlt_pipeline:
            mock_pipeline_instance = MagicMock()
            mock_load_info = MagicMock(has_failed_jobs=False)
            mock_pipeline_instance.run.return_value = mock_load_info
            mock_dlt_pipeline.return_value = mock_pipeline_instance

            # Run pipeline
            result = pipeline_module.run()

            # Verify result
            assert result is not None
            assert hasattr(result, "has_failed_jobs")
            assert not result.has_failed_jobs
