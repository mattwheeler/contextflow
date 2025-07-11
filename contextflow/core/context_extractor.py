"""
ContextFlow AI Context Extractor
Generic context extraction and formatting for any project type
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from .config import ContextFlowConfig


class ContextExtractor:
    """Generic AI context extractor for any project type"""
    
    def __init__(self, config: Optional[ContextFlowConfig] = None):
        self.config = config or ContextFlowConfig()
        self.config.ensure_directories()
        
        print("ContextFlow AI Context Extractor Initialized")
        print(f"Project: {self.config.project.name}")
        print(f"Type: {self.config.project.type}")
        print("=" * 50)
    
    def extract_and_generate_context(self) -> bool:
        """Extract context and generate AI-ready files"""
        try:
            print("Extracting and Generating AI Context...")

            # Gather project information
            project_context = self.gather_project_context()

            # Generate context files
            self.generate_quick_context(project_context)
            self.generate_full_context(project_context)
            self.generate_usage_instructions()

            print("AI context extraction and generation complete!")
            return True

        except Exception as e:
            print(f"Context extraction failed: {e}")
            return False
    
    def gather_project_context(self) -> Dict[str, Any]:
        """Gather comprehensive project context"""
        context = {
            'project': {
                'name': self.config.project.name,
                'description': self.config.project.description,
                'type': self.config.project.type,
                'version': self.config.project.version,
                'tags': self.config.project.tags
            },
            'integrations': self._get_enabled_integrations(),
            'file_structure': self._analyze_file_structure(),
            'recent_changes': self._get_recent_changes(),
            'work_items': self._get_recent_work_items(),
            'documentation': self._find_documentation_files(),
            'configuration': self._get_configuration_info(),
            'workflow': {
                'mandatory_updates': self.config.workflow.mandatory_session_updates,
                'work_item_references': self.config.workflow.require_work_item_references,
                'session_logs': str(self.config.get_session_log_directory()),
                'context_directory': str(self.config.get_context_directory())
            }
        }
        
        return context
    
    def _get_enabled_integrations(self) -> List[str]:
        """Get list of enabled integrations"""
        enabled = []
        
        for integration in ['confluence', 'jira', 'github', 'notion', 'slack']:
            if self.config.is_integration_enabled(integration):
                enabled.append(integration)
        
        return enabled
    
    def _analyze_file_structure(self) -> Dict[str, Any]:
        """Analyze project file structure"""
        project_root = Path.cwd()
        structure = {
            'root': str(project_root),
            'key_directories': [],
            'config_files': [],
            'documentation_files': [],
            'source_files': []
        }
        
        # Common important directories
        important_dirs = [
            'src', 'lib', 'app', 'components', 'pages', 'api',
            'docs', 'documentation', 'tests', 'test', 'spec',
            'config', 'configs', 'settings', 'scripts', 'tools',
            'assets', 'static', 'public', 'resources'
        ]
        
        for dir_name in important_dirs:
            dir_path = project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                structure['key_directories'].append(str(dir_path.relative_to(project_root)))
        
        # Common config files
        config_files = [
            'package.json', 'requirements.txt', 'Cargo.toml', 'go.mod',
            'pom.xml', 'build.gradle', 'Makefile', 'Dockerfile',
            'docker-compose.yml', '.env', '.env.example',
            'tsconfig.json', 'webpack.config.js', 'vite.config.js',
            'tailwind.config.js', 'next.config.js'
        ]
        
        for config_file in config_files:
            file_path = project_root / config_file
            if file_path.exists():
                structure['config_files'].append(config_file)
        
        # Documentation files
        doc_files = [
            'README.md', 'README.rst', 'CHANGELOG.md', 'CONTRIBUTING.md',
            'LICENSE', 'LICENSE.md', 'INSTALL.md', 'USAGE.md'
        ]
        
        for doc_file in doc_files:
            file_path = project_root / doc_file
            if file_path.exists():
                structure['documentation_files'].append(doc_file)
        
        return structure
    
    def _get_recent_changes(self) -> List[str]:
        """Get recent changes from session logs"""
        changes = []
        log_dir = self.config.get_session_log_directory()
        
        if log_dir.exists():
            # Get recent session logs (last 7 days)
            recent_logs = []
            cutoff_time = datetime.now().timestamp() - (7 * 24 * 60 * 60)
            
            for log_file in log_dir.glob("session_*.md"):
                if log_file.stat().st_mtime > cutoff_time:
                    recent_logs.append(log_file)
            
            # Sort by modification time (newest first)
            recent_logs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Extract summaries from recent logs
            for log_file in recent_logs[:5]:  # Last 5 sessions
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract the session summary section
                        summary_match = re.search(r'## Session Summary\n\n(.*?)\n\n', content, re.DOTALL)
                        if summary_match:
                            summary = summary_match.group(1).strip()
                            changes.append(f"Recent: {summary[:100]}...")
                except Exception:
                    continue
        
        return changes
    
    def _get_recent_work_items(self) -> List[str]:
        """Get recent work items from session logs"""
        work_items = set()
        log_dir = self.config.get_session_log_directory()
        
        if log_dir.exists():
            # Get recent session logs
            cutoff_time = datetime.now().timestamp() - (14 * 24 * 60 * 60)  # Last 2 weeks
            
            for log_file in log_dir.glob("session_*.md"):
                if log_file.stat().st_mtime > cutoff_time:
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Extract work items
                            work_item_section = re.search(r'### Work Items Referenced\n(.*?)\n\n', content, re.DOTALL)
                            if work_item_section:
                                items = re.findall(r'- (.+)', work_item_section.group(1))
                                work_items.update(items)
                    except Exception:
                        continue
        
        return list(work_items)
    
    def _find_documentation_files(self) -> List[str]:
        """Find key documentation files"""
        docs = []
        project_root = Path.cwd()
        
        # Look for documentation in common locations
        doc_patterns = [
            'README*',
            'docs/**/*.md',
            'documentation/**/*.md',
            '*.md'
        ]
        
        for pattern in doc_patterns:
            for file_path in project_root.glob(pattern):
                if file_path.is_file():
                    relative_path = str(file_path.relative_to(project_root))
                    if relative_path not in docs:
                        docs.append(relative_path)
        
        return docs[:10]  # Limit to top 10 most relevant
    
    def _get_configuration_info(self) -> Dict[str, Any]:
        """Get configuration information"""
        config_info = {
            'contextflow_config': str(self.config.config_path) if self.config.config_path else None,
            'project_type': self.config.project.type,
            'auto_refresh': self.config.ai_context.auto_refresh,
            'mandatory_updates': self.config.workflow.mandatory_session_updates
        }
        
        return config_info
    
    def generate_quick_context(self, project_context: Dict[str, Any]):
        """Generate quick AI context file"""
        context_dir = self.config.get_context_directory()
        quick_file = context_dir / self.config.ai_context.quick_context_file
        
        with open(quick_file, 'w', encoding='utf-8') as f:
            f.write(f"PROJECT: {project_context['project']['name']}\n")
            f.write(f"DESCRIPTION: {project_context['project']['description']}\n")
            f.write(f"TYPE: {project_context['project']['type']}\n")
            f.write(f"VERSION: {project_context['project']['version']}\n\n")
            
            if project_context['project']['tags']:
                f.write(f"TAGS: {', '.join(project_context['project']['tags'])}\n\n")
            
            f.write("INTEGRATIONS:\n")
            for integration in project_context['integrations']:
                f.write(f"- {integration.title()}: ENABLED\n")
            f.write("\n")
            
            f.write("KEY DIRECTORIES:\n")
            for directory in project_context['file_structure']['key_directories']:
                f.write(f"- {directory}\n")
            f.write("\n")
            
            f.write("CONFIGURATION FILES:\n")
            for config_file in project_context['file_structure']['config_files']:
                f.write(f"- {config_file}\n")
            f.write("\n")
            
            if project_context['recent_changes']:
                f.write("RECENT CHANGES:\n")
                for change in project_context['recent_changes'][:3]:
                    f.write(f"- {change}\n")
                f.write("\n")
            
            if project_context['work_items']:
                f.write("ACTIVE WORK ITEMS:\n")
                for item in project_context['work_items'][:5]:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            f.write("WORKFLOW SETTINGS:\n")
            f.write(f"- Mandatory session updates: {'YES' if project_context['workflow']['mandatory_updates'] else 'NO'}\n")
            f.write(f"- Work item references required: {'YES' if project_context['workflow']['work_item_references'] else 'NO'}\n")
            f.write(f"- Session logs: {project_context['workflow']['session_logs']}\n")
            f.write(f"- Context directory: {project_context['workflow']['context_directory']}\n\n")
            
            f.write("CONTEXTFLOW COMMANDS:\n")
            f.write("- Update session: contextflow update \"[session summary]\"\n")
            f.write("- Refresh context: contextflow context --refresh\n")
            f.write("- View logs: contextflow logs --recent\n")
        
        print(f"   📄 Quick context generated: {quick_file}")
    
    def generate_full_context(self, project_context: Dict[str, Any]):
        """Generate full AI context file"""
        context_dir = self.config.get_context_directory()
        full_file = context_dir / self.config.ai_context.full_context_file
        
        with open(full_file, 'w', encoding='utf-8') as f:
            f.write(f"# {project_context['project']['name']} - AI Context\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Project Type:** {project_context['project']['type']}\n\n")
            
            f.write("## 🎯 Project Overview\n\n")
            f.write(f"**Name:** {project_context['project']['name']}\n")
            f.write(f"**Description:** {project_context['project']['description']}\n")
            f.write(f"**Version:** {project_context['project']['version']}\n")
            if project_context['project']['tags']:
                f.write(f"**Tags:** {', '.join(project_context['project']['tags'])}\n")
            f.write("\n")
            
            f.write("## 🔗 Integrations\n\n")
            if project_context['integrations']:
                for integration in project_context['integrations']:
                    f.write(f"- **{integration.title()}:** Enabled\n")
            else:
                f.write("- No integrations currently enabled\n")
            f.write("\n")
            
            f.write("## 📁 Project Structure\n\n")
            f.write(f"**Root Directory:** {project_context['file_structure']['root']}\n\n")
            
            if project_context['file_structure']['key_directories']:
                f.write("**Key Directories:**\n")
                for directory in project_context['file_structure']['key_directories']:
                    f.write(f"- {directory}\n")
                f.write("\n")
            
            if project_context['file_structure']['config_files']:
                f.write("**Configuration Files:**\n")
                for config_file in project_context['file_structure']['config_files']:
                    f.write(f"- {config_file}\n")
                f.write("\n")
            
            if project_context['file_structure']['documentation_files']:
                f.write("**Documentation Files:**\n")
                for doc_file in project_context['file_structure']['documentation_files']:
                    f.write(f"- {doc_file}\n")
                f.write("\n")
            
            if project_context['recent_changes']:
                f.write("## 🔄 Recent Changes\n\n")
                for change in project_context['recent_changes']:
                    f.write(f"- {change}\n")
                f.write("\n")
            
            if project_context['work_items']:
                f.write("## 🎫 Active Work Items\n\n")
                for item in project_context['work_items']:
                    f.write(f"- {item}\n")
                f.write("\n")
            
            f.write("## ⚙️ Workflow Configuration\n\n")
            f.write(f"- **Mandatory session updates:** {'Enabled' if project_context['workflow']['mandatory_updates'] else 'Disabled'}\n")
            f.write(f"- **Work item references required:** {'Yes' if project_context['workflow']['work_item_references'] else 'No'}\n")
            f.write(f"- **Session logs directory:** {project_context['workflow']['session_logs']}\n")
            f.write(f"- **Context directory:** {project_context['workflow']['context_directory']}\n\n")
            
            f.write("## 🚀 ContextFlow Commands\n\n")
            f.write("```bash\n")
            f.write("# Update session documentation\n")
            f.write("contextflow update \"[detailed session summary]\"\n\n")
            f.write("# Refresh AI context\n")
            f.write("contextflow context --refresh\n\n")
            f.write("# View recent session logs\n")
            f.write("contextflow logs --recent\n\n")
            f.write("# Show project status\n")
            f.write("contextflow status\n")
            f.write("```\n\n")
            
            f.write("---\n\n")
            f.write("*This context file is automatically generated by ContextFlow. ")
            f.write("Use `contextflow context --refresh` to update with latest project information.*\n")
        
        print(f"   📄 Full context generated: {full_file}")
    
    def generate_usage_instructions(self):
        """Generate usage instructions file"""
        context_dir = self.config.get_context_directory()
        usage_file = context_dir / "HOW_TO_USE_CONTEXTFLOW.md"
        
        with open(usage_file, 'w', encoding='utf-8') as f:
            f.write("# How to Use ContextFlow\n\n")
            f.write("## 🎯 For New AI Sessions\n\n")
            f.write("### Quick Context (30 seconds)\n")
            f.write("```bash\n")
            f.write(f"cat {self.config.ai_context.quick_context_file}\n")
            f.write("```\n")
            f.write("Copy the output and paste into new AI session.\n\n")
            
            f.write("### Complete Context\n")
            f.write("```bash\n")
            f.write(f"cat {self.config.ai_context.full_context_file}\n")
            f.write("```\n")
            f.write("Use for comprehensive project understanding.\n\n")
            
            f.write("## 🔄 End of Session (MANDATORY)\n\n")
            f.write("```bash\n")
            f.write("contextflow update \"[your session summary]\"\n")
            f.write("```\n\n")
            
            f.write("**Include in your summary:**\n")
            f.write("- Work items referenced (tickets, issues, tasks)\n")
            f.write("- Files created or modified\n")
            f.write("- Features added or bugs fixed\n")
            f.write("- Architecture or design changes\n\n")
            
            f.write("## 📊 Other Commands\n\n")
            f.write("```bash\n")
            f.write("# Refresh context\n")
            f.write("contextflow context --refresh\n\n")
            f.write("# View recent logs\n")
            f.write("contextflow logs --recent\n\n")
            f.write("# Show project status\n")
            f.write("contextflow status\n")
            f.write("```\n")
        
        print(f"   📖 Usage instructions generated: {usage_file}")
