import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import contextflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from click.testing import CliRunner
    from contextflow.cli import main
except ImportError:
    # Skip tests if dependencies not available
    import pytest

    pytest.skip("contextflow dependencies not available", allow_module_level=True)


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_main_help(self):
        """Test main command help"""
        result = self.runner.invoke(main, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("ContextFlow", result.output)

    def test_templates_command(self):
        """Test templates command"""
        result = self.runner.invoke(main, ["templates"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("software-development", result.output)
        self.assertIn("side-project", result.output)

    @patch("contextflow.cli.ContextFlowConfig")
    def test_credentials_command_empty(self, mock_config):
        """Test credentials command with no stored credentials"""
        mock_instance = MagicMock()
        mock_instance.list_stored_credentials.return_value = {}
        mock_config.return_value = mock_instance

        result = self.runner.invoke(main, ["credentials"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No credentials stored", result.output)

    @patch("contextflow.cli.ContextFlowConfig")
    def test_credentials_command_with_data(self, mock_config):
        """Test credentials command with stored credentials"""
        mock_instance = MagicMock()
        mock_instance.list_stored_credentials.return_value = {
            "github": ["token"],
            "jira": ["username", "api_token"],
        }
        mock_config.return_value = mock_instance

        result = self.runner.invoke(main, ["credentials"])
        self.assertEqual(result.exit_code, 0)
        # Check for case-insensitive match since Rich may capitalize
        output_lower = result.output.lower()
        self.assertIn("github", output_lower)
        self.assertIn("jira", output_lower)

    def test_invalid_setup_integration(self):
        """Test setup command with invalid integration"""
        result = self.runner.invoke(main, ["setup", "invalid"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid integration", result.output)


if __name__ == "__main__":
    unittest.main()
