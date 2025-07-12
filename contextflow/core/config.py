"""
ContextFlow Configuration Management
"""

import os
import yaml
import keyring
import getpass
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ProjectConfig:
    """Project configuration settings"""

    name: str = "My Project"
    description: str = "Project description"
    type: str = "software-development"
    version: str = "1.0.0"
    tags: list = field(default_factory=list)


@dataclass
class IntegrationConfig:
    """Integration configuration settings"""

    confluence: Dict[str, Any] = field(default_factory=dict)
    jira: Dict[str, Any] = field(default_factory=dict)
    github: Dict[str, Any] = field(default_factory=dict)
    notion: Dict[str, Any] = field(default_factory=dict)
    slack: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIContextConfig:
    """AI context configuration settings"""

    quick_context_file: str = "QUICK_CONTEXT.txt"
    full_context_file: str = "PROJECT_CONTEXT.md"
    context_directory: str = "ai-context"
    auto_refresh: bool = True
    max_context_length: int = 10000
    include_recent_changes: bool = True


@dataclass
class WorkflowConfig:
    """Workflow configuration settings"""

    mandatory_session_updates: bool = True
    require_work_item_references: bool = True
    session_log_retention_days: int = 90
    team_notifications: bool = False
    auto_archive_logs: bool = True
    session_log_directory: str = "session-logs"


class ContextFlowConfig:
    """Main ContextFlow configuration manager with secure secrets handling"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_file()
        self.project = ProjectConfig()
        self.integrations = IntegrationConfig()
        self.ai_context = AIContextConfig()
        self.workflow = WorkflowConfig()
        self._keyring_service = "contextflow"

        if self.config_path and os.path.exists(self.config_path):
            self.load_config()

    def _find_config_file(self) -> Optional[str]:
        """Find the configuration file in the current directory or parents"""
        current_dir = Path.cwd()

        # Look for config files in order of preference
        config_names = [
            "contextflow.yaml",
            "contextflow.yml",
            ".contextflow.yaml",
            ".contextflow.yml",
        ]

        # Search current directory and parents
        for parent in [current_dir] + list(current_dir.parents):
            for config_name in config_names:
                config_path = parent / config_name
                if config_path.exists():
                    return str(config_path)

        return None

    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f) or {}

            # Load project config
            if "project" in config_data:
                project_data = config_data["project"]
                self.project = ProjectConfig(
                    name=project_data.get("name", self.project.name),
                    description=project_data.get("description", self.project.description),
                    type=project_data.get("type", self.project.type),
                    version=project_data.get("version", self.project.version),
                    tags=project_data.get("tags", self.project.tags),
                )

            # Load integration config
            if "integrations" in config_data:
                integration_data = config_data["integrations"]
                self.integrations = IntegrationConfig(
                    confluence=integration_data.get("confluence", {}),
                    jira=integration_data.get("jira", {}),
                    github=integration_data.get("github", {}),
                    notion=integration_data.get("notion", {}),
                    slack=integration_data.get("slack", {}),
                )

            # Load AI context config
            if "ai_context" in config_data:
                ai_data = config_data["ai_context"]
                self.ai_context = AIContextConfig(
                    quick_context_file=ai_data.get(
                        "quick_context_file", self.ai_context.quick_context_file
                    ),
                    full_context_file=ai_data.get(
                        "full_context_file", self.ai_context.full_context_file
                    ),
                    context_directory=ai_data.get(
                        "context_directory", self.ai_context.context_directory
                    ),
                    auto_refresh=ai_data.get("auto_refresh", self.ai_context.auto_refresh),
                    max_context_length=ai_data.get(
                        "max_context_length", self.ai_context.max_context_length
                    ),
                    include_recent_changes=ai_data.get(
                        "include_recent_changes", self.ai_context.include_recent_changes
                    ),
                )

            # Load workflow config
            if "workflow" in config_data:
                workflow_data = config_data["workflow"]
                self.workflow = WorkflowConfig(
                    mandatory_session_updates=workflow_data.get(
                        "mandatory_session_updates", self.workflow.mandatory_session_updates
                    ),
                    require_work_item_references=workflow_data.get(
                        "require_work_item_references", self.workflow.require_work_item_references
                    ),
                    session_log_retention_days=workflow_data.get(
                        "session_log_retention_days", self.workflow.session_log_retention_days
                    ),
                    team_notifications=workflow_data.get(
                        "team_notifications", self.workflow.team_notifications
                    ),
                    auto_archive_logs=workflow_data.get(
                        "auto_archive_logs", self.workflow.auto_archive_logs
                    ),
                    session_log_directory=workflow_data.get(
                        "session_log_directory", self.workflow.session_log_directory
                    ),
                )

        except Exception as e:
            print(f"Warning: Could not load config file {self.config_path}: {e}")

    def save_config(self, config_path: Optional[str] = None):
        """Save current configuration to YAML file"""
        save_path = config_path or self.config_path or "contextflow.yaml"

        config_data = {
            "project": {
                "name": self.project.name,
                "description": self.project.description,
                "type": self.project.type,
                "version": self.project.version,
                "tags": self.project.tags,
            },
            "integrations": {
                "confluence": self.integrations.confluence,
                "jira": self.integrations.jira,
                "github": self.integrations.github,
                "notion": self.integrations.notion,
                "slack": self.integrations.slack,
            },
            "ai_context": {
                "quick_context_file": self.ai_context.quick_context_file,
                "full_context_file": self.ai_context.full_context_file,
                "context_directory": self.ai_context.context_directory,
                "auto_refresh": self.ai_context.auto_refresh,
                "max_context_length": self.ai_context.max_context_length,
                "include_recent_changes": self.ai_context.include_recent_changes,
            },
            "workflow": {
                "mandatory_session_updates": self.workflow.mandatory_session_updates,
                "require_work_item_references": self.workflow.require_work_item_references,
                "session_log_retention_days": self.workflow.session_log_retention_days,
                "team_notifications": self.workflow.team_notifications,
                "auto_archive_logs": self.workflow.auto_archive_logs,
                "session_log_directory": self.workflow.session_log_directory,
            },
        }

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            print(f"Configuration saved to {save_path}")
        except Exception as e:
            print(f"Error saving config to {save_path}: {e}")

    def get_integration_config(self, integration_name: str) -> Dict[str, Any]:
        """Get configuration for a specific integration"""
        return getattr(self.integrations, integration_name, {})

    def is_integration_enabled(self, integration_name: str) -> bool:
        """Check if an integration is enabled"""
        config = self.get_integration_config(integration_name)
        return config.get("enabled", False)

    def get_context_directory(self) -> Path:
        """Get the full path to the context directory"""
        return Path.cwd() / self.ai_context.context_directory

    def get_session_log_directory(self) -> Path:
        """Get the full path to the session log directory"""
        return Path.cwd() / self.workflow.session_log_directory

    def ensure_directories(self):
        """Ensure required directories exist"""
        self.get_context_directory().mkdir(exist_ok=True)
        self.get_session_log_directory().mkdir(exist_ok=True)

    def set_credential(self, integration: str, credential_type: str, value: str):
        """Securely store a credential using keyring"""
        key = f"{integration}_{credential_type}"
        keyring.set_password(self._keyring_service, key, value)
        print(f"Credential stored securely for {integration} {credential_type}")

    def get_credential(self, integration: str, credential_type: str) -> Optional[str]:
        """Securely retrieve a credential using keyring"""
        key = f"{integration}_{credential_type}"
        try:
            return keyring.get_password(self._keyring_service, key)
        except Exception as e:
            # Silently handle keyring errors (credential doesn't exist, access denied, etc.)
            return None

    def prompt_for_credential(
        self, integration: str, credential_type: str, prompt_text: str
    ) -> str:
        """Prompt user for credential and store it securely"""
        if credential_type in ["password", "token", "api_token"]:
            value = getpass.getpass(f"{prompt_text}: ")
        else:
            value = input(f"{prompt_text}: ")

        if value:
            self.set_credential(integration, credential_type, value)

        return value

    def get_integration_credentials(self, integration_name: str) -> Dict[str, str]:
        """Get all credentials for an integration"""
        config = self.get_integration_config(integration_name)
        credentials = {}

        # Common credential types
        credential_types = ["username", "password", "api_token", "token"]

        for cred_type in credential_types:
            # Always try to get from keyring first (credentials should be stored there)
            stored_value = self.get_credential(integration_name, cred_type)
            if stored_value:
                credentials[cred_type] = stored_value
            elif cred_type in config and config[cred_type]:  # Fallback to config file (for migration)
                credentials[cred_type] = config[cred_type]

        return credentials

    def setup_integration_credentials(self, integration_name: str):
        """Interactive setup for integration credentials"""
        print(f"\nSetting up credentials for {integration_name.title()}")

        if integration_name == "confluence":
            username = self.prompt_for_credential(
                "confluence", "username", "Confluence username/email"
            )
            api_token = self.prompt_for_credential(
                "confluence", "api_token", "Confluence API token"
            )

        elif integration_name == "jira":
            username = self.prompt_for_credential("jira", "username", "JIRA username/email")
            api_token = self.prompt_for_credential("jira", "api_token", "JIRA API token")

        elif integration_name == "github":
            token = self.prompt_for_credential("github", "token", "GitHub personal access token")

        elif integration_name == "notion":
            token = self.prompt_for_credential("notion", "token", "Notion integration token")

        elif integration_name == "slack":
            token = self.prompt_for_credential("slack", "token", "Slack bot token")

        print(f"Credentials for {integration_name.title()} stored securely!")

    def remove_credentials(self, integration_name: str):
        """Remove stored credentials for an integration"""
        credential_types = ["username", "password", "api_token", "token"]

        for cred_type in credential_types:
            try:
                key = f"{integration_name}_{cred_type}"
                keyring.delete_password(self._keyring_service, key)
            except keyring.errors.PasswordDeleteError:
                pass  # Credential doesn't exist

        print(f"Credentials removed for {integration_name.title()}")

    def list_stored_credentials(self) -> Dict[str, list]:
        """List which integrations have stored credentials"""
        integrations = ["confluence", "jira", "github", "notion", "slack"]
        credential_types = ["username", "api_token", "token"]

        stored = {}

        for integration in integrations:
            stored_creds = []
            for cred_type in credential_types:
                if self.get_credential(integration, cred_type):
                    stored_creds.append(cred_type)

            if stored_creds:
                stored[integration] = stored_creds

        return stored
