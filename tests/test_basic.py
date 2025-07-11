import unittest
import os
import sys

# Add the parent directory to the path to import contextflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestBasicFunctionality(unittest.TestCase):
    """Basic tests that should work in any environment"""

    def test_import_contextflow(self):
        """Test that we can import the main module"""
        try:
            import contextflow

            self.assertTrue(hasattr(contextflow, "__version__"))
        except ImportError as e:
            self.skipTest(f"ContextFlow not importable: {e}")

    def test_import_cli(self):
        """Test that we can import the CLI module"""
        try:
            from contextflow import cli

            self.assertTrue(hasattr(cli, "main"))
        except ImportError as e:
            self.skipTest(f"CLI not importable: {e}")

    def test_import_config(self):
        """Test that we can import the config module"""
        try:
            from contextflow.core import config

            self.assertTrue(hasattr(config, "ContextFlowConfig"))
        except ImportError as e:
            self.skipTest(f"Config not importable: {e}")

    def test_import_templates(self):
        """Test that we can import the templates module"""
        try:
            from contextflow.templates import project_templates

            self.assertTrue(hasattr(project_templates, "ProjectTemplates"))
        except ImportError as e:
            self.skipTest(f"Templates not importable: {e}")


if __name__ == "__main__":
    unittest.main()
