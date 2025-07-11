import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import contextflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from contextflow.core.config import ContextFlowConfig
except ImportError:
    # Skip tests if dependencies not available
    import pytest

    pytest.skip("contextflow dependencies not available", allow_module_level=True)


class TestContextFlowConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "contextflow.yaml")

    def test_config_initialization(self):
        """Test basic config initialization"""
        config = ContextFlowConfig()
        self.assertIsNotNone(config.project)
        self.assertIsNotNone(config.integrations)
        self.assertIsNotNone(config.ai_context)
        self.assertIsNotNone(config.workflow)

    def test_config_with_file(self):
        """Test config loading from file"""
        # Create a basic config file
        config_content = """
project:
  name: "Test Project"
  description: "Test Description"
  type: "software-development"

integrations:
  github:
    enabled: true
    repository: "test/repo"

ai_context:
  quick_context_file: "QUICK_CONTEXT.txt"
  auto_refresh: true

workflow:
  mandatory_session_updates: true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ContextFlowConfig(self.config_file)
        self.assertEqual(config.project.name, "Test Project")
        self.assertEqual(config.project.description, "Test Description")
        self.assertEqual(config.project.type, "software-development")

    def test_integration_enabled(self):
        """Test integration enabled check"""
        config = ContextFlowConfig()
        config.integrations.github = {"enabled": True}
        self.assertTrue(config.is_integration_enabled("github"))

        config.integrations.jira = {"enabled": False}
        self.assertFalse(config.is_integration_enabled("jira"))

    def test_get_integration_config(self):
        """Test getting integration config"""
        config = ContextFlowConfig()
        config.integrations.github = {"enabled": True, "repository": "test/repo"}

        github_config = config.get_integration_config("github")
        self.assertEqual(github_config["repository"], "test/repo")

    def test_ensure_directories(self):
        """Test directory creation"""
        config = ContextFlowConfig()
        config.ai_context.context_directory = "test-context"
        config.workflow.session_log_directory = "test-logs"

        # Change to temp directory
        old_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        try:
            config.ensure_directories()
            self.assertTrue(Path("test-context").exists())
            self.assertTrue(Path("test-logs").exists())
        finally:
            os.chdir(old_cwd)

    def tearDown(self):
        # Clean up temp files
        import shutil

        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    unittest.main()
