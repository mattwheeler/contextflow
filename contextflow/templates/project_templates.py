"""
ContextFlow Project Templates
Pre-configured templates for different project types
"""

from typing import Dict, Any
from ..core.config import ContextFlowConfig


class ProjectTemplates:
    """Manage project templates for different use cases"""
    
    def __init__(self):
        self.templates = {
            'software-development': {
                'description': 'Software development with JIRA, GitHub, and technical documentation',
                'integrations': ['jira', 'github', 'confluence'],
                'config': self._software_development_template
            },
            'side-project': {
                'description': 'Personal side projects with simple tracking and GitHub integration',
                'integrations': ['github'],
                'config': self._side_project_template
            },
            'research-project': {
                'description': 'Research projects with literature tracking and experiment logs',
                'integrations': ['notion', 'github'],
                'config': self._research_project_template
            },
            'consulting': {
                'description': 'Client consulting with deliverable tracking and meeting management',
                'integrations': ['confluence', 'slack'],
                'config': self._consulting_project_template
            },
            'content-creation': {
                'description': 'Content creation with editorial calendars and progress tracking',
                'integrations': ['notion'],
                'config': self._content_creation_template
            },
            'academic-research': {
                'description': 'Academic research with paper writing and citation management',
                'integrations': ['github', 'notion'],
                'config': self._academic_research_template
            },
            'minimal': {
                'description': 'Minimal setup with basic session tracking only',
                'integrations': [],
                'config': self._minimal_template
            }
        }
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all available templates"""
        return {name: {'description': info['description'], 'integrations': info['integrations']} 
                for name, info in self.templates.items()}
    
    def create_project_from_template(self, template_name: str, project_name: str, description: str) -> ContextFlowConfig:
        """Create a new project from template"""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template_info = self.templates[template_name]
        config = ContextFlowConfig()
        
        # Apply template configuration
        template_info['config'](config, project_name, description)
        
        # Save configuration
        config.save_config()
        
        return config
    
    def _software_development_template(self, config: ContextFlowConfig, name: str, description: str):
        """Software development template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "software-development"
        config.project.tags = ["development", "software", "engineering"]
        
        # Enable relevant integrations (credentials stored securely)
        config.integrations.jira = {
            'enabled': True,
            'base_url': 'https://your-company.atlassian.net',
            'project_key': 'PROJ'
        }

        config.integrations.github = {
            'enabled': True,
            'repository': 'your-org/your-repo'
        }

        config.integrations.confluence = {
            'enabled': True,
            'base_url': 'https://your-company.atlassian.net',
            'space_key': 'PROJ'
        }
        
        # Workflow settings for development
        config.workflow.mandatory_session_updates = True
        config.workflow.require_work_item_references = True
        config.workflow.session_log_retention_days = 90
        
        # AI context settings
        config.ai_context.quick_context_file = "DEV_QUICK_CONTEXT.txt"
        config.ai_context.full_context_file = "DEV_PROJECT_CONTEXT.md"
        config.ai_context.auto_refresh = True

    def _side_project_template(self, config: ContextFlowConfig, name: str, description: str):
        """Side project template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "side-project"
        config.project.tags = ["side-project", "personal", "hobby"]

        # Enable GitHub for code tracking (credentials stored securely)
        config.integrations.github = {
            'enabled': True,
            'repository': 'your-username/your-repo'
        }

        # Disable other integrations for simplicity
        config.integrations.jira = {'enabled': False}
        config.integrations.confluence = {'enabled': False}
        config.integrations.notion = {'enabled': False}
        config.integrations.slack = {'enabled': False}

        # Relaxed workflow settings for personal projects
        config.workflow.mandatory_session_updates = True
        config.workflow.require_work_item_references = False  # More flexible for personal projects
        config.workflow.session_log_retention_days = 60
        config.workflow.team_notifications = False

        # Side project context
        config.ai_context.quick_context_file = "SIDE_PROJECT_CONTEXT.txt"
        config.ai_context.full_context_file = "SIDE_PROJECT_FULL.md"
        config.ai_context.auto_refresh = True

    def _research_project_template(self, config: ContextFlowConfig, name: str, description: str):
        """Research project template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "research-project"
        config.project.tags = ["research", "academic", "science"]
        
        # Enable research-focused integrations
        config.integrations.notion = {
            'enabled': True,
            'token': '',
            'database_id': ''
        }
        
        config.integrations.github = {
            'enabled': True,
            'repository': 'your-org/research-repo',
            'token': ''
        }
        
        # Research workflow settings
        config.workflow.mandatory_session_updates = True
        config.workflow.require_work_item_references = False  # More flexible for research
        config.workflow.session_log_retention_days = 365  # Longer retention for research
        
        # Research-focused context
        config.ai_context.quick_context_file = "RESEARCH_QUICK_CONTEXT.txt"
        config.ai_context.full_context_file = "RESEARCH_PROJECT_CONTEXT.md"
        config.ai_context.auto_refresh = True
    
    def _consulting_project_template(self, config: ContextFlowConfig, name: str, description: str):
        """Consulting project template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "consulting-project"
        config.project.tags = ["consulting", "client", "deliverables"]
        
        # Enable client-focused integrations
        config.integrations.confluence = {
            'enabled': True,
            'base_url': 'https://your-company.atlassian.net',
            'space_key': 'CLIENT',
            'username': '',
            'api_token': ''
        }
        
        config.integrations.slack = {
            'enabled': True,
            'token': '',
            'channel': '#client-project'
        }
        
        # Consulting workflow settings
        config.workflow.mandatory_session_updates = True
        config.workflow.require_work_item_references = False
        config.workflow.session_log_retention_days = 180
        config.workflow.team_notifications = True
        
        # Client-focused context
        config.ai_context.quick_context_file = "CLIENT_QUICK_CONTEXT.txt"
        config.ai_context.full_context_file = "CLIENT_PROJECT_CONTEXT.md"
        config.ai_context.auto_refresh = True
    
    def _content_creation_template(self, config: ContextFlowConfig, name: str, description: str):
        """Content creation template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "content-creation"
        config.project.tags = ["content", "marketing", "creative"]
        
        # Enable content-focused integrations
        config.integrations.notion = {
            'enabled': True,
            'token': '',
            'database_id': ''
        }
        
        config.integrations.slack = {
            'enabled': True,
            'token': '',
            'channel': '#content-team'
        }
        
        # Content workflow settings
        config.workflow.mandatory_session_updates = True
        config.workflow.require_work_item_references = False
        config.workflow.session_log_retention_days = 120
        
        # Content-focused context
        config.ai_context.quick_context_file = "CONTENT_QUICK_CONTEXT.txt"
        config.ai_context.full_context_file = "CONTENT_PROJECT_CONTEXT.md"
        config.ai_context.auto_refresh = True
    
    def _startup_project_template(self, config: ContextFlowConfig, name: str, description: str):
        """Startup project template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "startup-project"
        config.project.tags = ["startup", "mvp", "growth"]
        
        # Enable startup-focused integrations
        config.integrations.github = {
            'enabled': True,
            'repository': 'startup-org/product-repo',
            'token': ''
        }
        
        config.integrations.notion = {
            'enabled': True,
            'token': '',
            'database_id': ''
        }
        
        config.integrations.slack = {
            'enabled': True,
            'token': '',
            'channel': '#general'
        }
        
        # Startup workflow settings
        config.workflow.mandatory_session_updates = True
        config.workflow.require_work_item_references = False
        config.workflow.session_log_retention_days = 180
        config.workflow.team_notifications = True
        
        # Startup-focused context
        config.ai_context.quick_context_file = "STARTUP_QUICK_CONTEXT.txt"
        config.ai_context.full_context_file = "STARTUP_PROJECT_CONTEXT.md"
        config.ai_context.auto_refresh = True
    
    def _academic_research_template(self, config: ContextFlowConfig, name: str, description: str):
        """Academic research template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "academic-research"
        config.project.tags = ["academic", "research", "publication"]
        
        # Enable academic-focused integrations
        config.integrations.github = {
            'enabled': True,
            'repository': 'research-group/paper-repo',
            'token': ''
        }
        
        config.integrations.notion = {
            'enabled': True,
            'token': '',
            'database_id': ''
        }
        
        # Academic workflow settings
        config.workflow.mandatory_session_updates = True
        config.workflow.require_work_item_references = False
        config.workflow.session_log_retention_days = 730  # 2 years for academic work
        
        # Academic-focused context
        config.ai_context.quick_context_file = "ACADEMIC_QUICK_CONTEXT.txt"
        config.ai_context.full_context_file = "ACADEMIC_PROJECT_CONTEXT.md"
        config.ai_context.auto_refresh = True
    
    def _minimal_template(self, config: ContextFlowConfig, name: str, description: str):
        """Minimal template configuration"""
        config.project.name = name
        config.project.description = description
        config.project.type = "minimal"
        config.project.tags = ["minimal", "basic"]
        
        # No integrations enabled
        config.integrations.confluence = {'enabled': False}
        config.integrations.jira = {'enabled': False}
        config.integrations.github = {'enabled': False}
        config.integrations.notion = {'enabled': False}
        config.integrations.slack = {'enabled': False}
        
        # Basic workflow settings
        config.workflow.mandatory_session_updates = False
        config.workflow.require_work_item_references = False
        config.workflow.session_log_retention_days = 30
        
        # Basic context
        config.ai_context.quick_context_file = "QUICK_CONTEXT.txt"
        config.ai_context.full_context_file = "PROJECT_CONTEXT.md"
        config.ai_context.auto_refresh = False
