import unittest
import tempfile
import os
from contextflow.templates.project_templates import ProjectTemplates


class TestProjectTemplates(unittest.TestCase):
    
    def setUp(self):
        self.templates = ProjectTemplates()
        self.temp_dir = tempfile.mkdtemp()
        
    def test_get_available_templates(self):
        """Test getting available templates"""
        templates = self.templates.get_available_templates()
        self.assertIsInstance(templates, dict)
        self.assertIn('software-development', templates)
        self.assertIn('side-project', templates)
        self.assertIn('minimal', templates)
        
    def test_template_structure(self):
        """Test template structure"""
        templates = self.templates.get_available_templates()
        
        for name, template in templates.items():
            self.assertIn('description', template)
            self.assertIn('integrations', template)
            self.assertIn('config', template)
            self.assertIsInstance(template['description'], str)
            self.assertIsInstance(template['integrations'], list)
            
    def test_create_software_development_project(self):
        """Test creating software development project"""
        old_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            config = self.templates.create_project_from_template(
                'software-development',
                'Test Project',
                'Test Description'
            )
            
            self.assertIsNotNone(config)
            self.assertEqual(config.project.name, 'Test Project')
            self.assertEqual(config.project.description, 'Test Description')
            self.assertEqual(config.project.type, 'software-development')
            
            # Check that config file was created
            self.assertTrue(os.path.exists('contextflow.yaml'))
            
        finally:
            os.chdir(old_cwd)
            
    def test_create_side_project(self):
        """Test creating side project"""
        old_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            config = self.templates.create_project_from_template(
                'side-project',
                'My Side Project',
                'Personal project'
            )
            
            self.assertIsNotNone(config)
            self.assertEqual(config.project.name, 'My Side Project')
            self.assertEqual(config.project.type, 'side-project')
            
            # Side projects should have relaxed workflow
            self.assertFalse(config.workflow.require_work_item_references)
            
        finally:
            os.chdir(old_cwd)
            
    def test_invalid_template(self):
        """Test creating project with invalid template"""
        config = self.templates.create_project_from_template(
            'invalid-template',
            'Test',
            'Test'
        )
        self.assertIsNone(config)
        
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()
