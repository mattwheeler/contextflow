"""
ContextFlow Session Documentation Updater
Generic session documentation and workflow automation
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from .config import ContextFlowConfig
from ..integrations.confluence import ConfluenceIntegration
from ..integrations.jira import JiraIntegration
from ..integrations.github import GitHubIntegration


class SessionUpdater:
    """Generic session documentation updater for any project type"""

    def __init__(self, config: Optional[ContextFlowConfig] = None):
        self.config = config or ContextFlowConfig()
        self.config.ensure_directories()

        # Initialize integrations based on configuration
        self.integrations = {}
        self._initialize_integrations()

        print("ContextFlow Session Updater Initialized")
        print(f"Project: {self.config.project.name}")
        print(f"Type: {self.config.project.type}")
        print("=" * 50)

    def _initialize_integrations(self):
        """Initialize enabled integrations"""
        if self.config.is_integration_enabled("confluence"):
            try:
                self.integrations["confluence"] = ConfluenceIntegration(
                    self.config.get_integration_config("confluence"), self.config
                )
                print("Confluence integration enabled")
            except Exception as e:
                print(f"Confluence integration failed: {e}")

        if self.config.is_integration_enabled("jira"):
            try:
                self.integrations["jira"] = JiraIntegration(
                    self.config.get_integration_config("jira"), self.config
                )
                print("JIRA integration enabled")
            except Exception as e:
                print(f"JIRA integration failed: {e}")

        if self.config.is_integration_enabled("github"):
            try:
                self.integrations["github"] = GitHubIntegration(
                    self.config.get_integration_config("github"), self.config
                )
                print("GitHub integration enabled")
            except Exception as e:
                print(f"GitHub integration failed: {e}")

    def update_session_documentation(self, session_summary: str) -> bool:
        """Update documentation based on session work"""
        try:
            print("Updating Documentation from Session...")

            # Parse session summary
            updates = self.parse_session_summary(session_summary)

            # Update integrations
            success_count = 0
            total_integrations = len(self.integrations)

            for integration_name, integration in self.integrations.items():
                try:
                    if hasattr(integration, "update_from_session"):
                        integration.update_from_session(updates)
                        print(f"   {integration_name.title()} updated")
                        success_count += 1
                    else:
                        print(f"   {integration_name.title()} doesn't support session updates")
                except Exception as e:
                    print(f"   {integration_name.title()} update failed: {e}")

            # Create session log
            self.create_session_log(session_summary, updates)

            # Refresh AI context if configured
            if self.config.ai_context.auto_refresh:
                self.refresh_ai_context()

            print(
                f"Session documentation updated! ({success_count}/{total_integrations} integrations)"
            )
            return True

        except Exception as e:
            print(f"Documentation update failed: {e}")
            return False

    def parse_session_summary(self, session_summary: str) -> Dict[str, Any]:
        """Parse session summary to determine what needs updating"""
        updates = {
            "summary": session_summary,
            "timestamp": datetime.now().isoformat(),
            "project_type": self.config.project.type,
            "work_items": [],
            "files_changed": [],
            "features_added": [],
            "bugs_fixed": [],
            "architecture_changes": [],
            "documentation_updates": [],
            "categories": [],
        }

        # Extract work item references (flexible patterns)
        work_item_patterns = [
            r"[A-Z]+-\d+",  # JIRA-style (PROJ-123)
            r"#\d+",  # GitHub-style (#123)
            r"issue-\d+",  # Generic issue references
            r"task-\d+",  # Generic task references
        ]

        for pattern in work_item_patterns:
            matches = re.findall(pattern, session_summary, re.IGNORECASE)
            updates["work_items"].extend(matches)

        # Extract file changes (flexible patterns)
        file_patterns = [
            r"[a-zA-Z0-9/_.-]+\.[a-zA-Z]+",  # File paths with extensions
            r"src/[a-zA-Z0-9/_.-]+",  # Source files
            r"docs/[a-zA-Z0-9/_.-]+",  # Documentation files
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, session_summary)
            updates["files_changed"].extend(matches)

        # Categorize changes based on keywords
        summary_lower = session_summary.lower()

        # Features
        if any(
            term in summary_lower
            for term in ["implemented", "added", "created", "new feature", "enhancement"]
        ):
            updates["categories"].append("feature")
            updates["features_added"] = self.extract_features(session_summary)

        # Bug fixes
        if any(term in summary_lower for term in ["fixed", "resolved", "bug", "issue", "error"]):
            updates["categories"].append("bugfix")
            updates["bugs_fixed"] = self.extract_bug_fixes(session_summary)

        # Architecture changes
        if any(
            term in summary_lower for term in ["architecture", "design", "refactor", "restructure"]
        ):
            updates["categories"].append("architecture")
            updates["architecture_changes"] = self.extract_architecture_changes(session_summary)

        # Documentation updates
        if any(term in summary_lower for term in ["documentation", "docs", "readme", "guide"]):
            updates["categories"].append("documentation")
            updates["documentation_updates"] = self.extract_documentation_updates(session_summary)

        # Remove duplicates
        updates["work_items"] = list(set(updates["work_items"]))
        updates["files_changed"] = list(set(updates["files_changed"]))
        updates["categories"] = list(set(updates["categories"]))

        return updates

    def extract_features(self, session_summary: str) -> List[str]:
        """Extract feature descriptions from session summary"""
        features = []
        lines = session_summary.split("\n")

        for line in lines:
            line_lower = line.lower()
            if any(term in line_lower for term in ["implemented", "added", "created", "new"]):
                if any(
                    feature_term in line_lower
                    for feature_term in ["feature", "component", "function", "endpoint", "page"]
                ):
                    features.append(line.strip())

        return features

    def extract_bug_fixes(self, session_summary: str) -> List[str]:
        """Extract bug fix descriptions from session summary"""
        fixes = []
        lines = session_summary.split("\n")

        for line in lines:
            line_lower = line.lower()
            if any(term in line_lower for term in ["fixed", "resolved", "corrected"]):
                fixes.append(line.strip())

        return fixes

    def extract_architecture_changes(self, session_summary: str) -> List[str]:
        """Extract architecture change descriptions"""
        changes = []
        lines = session_summary.split("\n")

        for line in lines:
            line_lower = line.lower()
            if any(
                term in line_lower
                for term in ["architecture", "design", "refactor", "restructure", "migrate"]
            ):
                changes.append(line.strip())

        return changes

    def extract_documentation_updates(self, session_summary: str) -> List[str]:
        """Extract documentation update descriptions"""
        updates = []
        lines = session_summary.split("\n")

        for line in lines:
            line_lower = line.lower()
            if any(
                term in line_lower
                for term in ["documentation", "docs", "readme", "guide", "manual"]
            ):
                updates.append(line.strip())

        return updates

    def create_session_log(self, session_summary: str, updates: Dict[str, Any]):
        """Create a log of the session for tracking"""
        log_dir = self.config.get_session_log_directory()
        log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"session_{timestamp}.md"

        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"# ContextFlow Session Log\n\n")
            f.write(f"**Project:** {self.config.project.name}\n")
            f.write(f"**Type:** {self.config.project.type}\n")
            f.write(f"**Timestamp:** {updates['timestamp']}\n\n")

            f.write("## Session Summary\n\n")
            f.write(f"{session_summary}\n\n")

            f.write("## Parsed Updates\n\n")
            f.write(f"**Categories:** {', '.join(updates['categories'])}\n")
            f.write(f"**Work Items:** {len(updates['work_items'])}\n")
            f.write(f"**Files Changed:** {len(updates['files_changed'])}\n")
            f.write(f"**Features Added:** {len(updates['features_added'])}\n")
            f.write(f"**Bugs Fixed:** {len(updates['bugs_fixed'])}\n\n")

            if updates["work_items"]:
                f.write("### Work Items Referenced\n")
                for item in updates["work_items"]:
                    f.write(f"- {item}\n")
                f.write("\n")

            if updates["files_changed"]:
                f.write("### Files Changed\n")
                for file in updates["files_changed"]:
                    f.write(f"- {file}\n")
                f.write("\n")

            if updates["features_added"]:
                f.write("### Features Added\n")
                for feature in updates["features_added"]:
                    f.write(f"- {feature}\n")
                f.write("\n")

            if updates["bugs_fixed"]:
                f.write("### Bugs Fixed\n")
                for bug in updates["bugs_fixed"]:
                    f.write(f"- {bug}\n")
                f.write("\n")

        print(f"   📝 Session log created: {log_file}")
        return log_file

    def refresh_ai_context(self):
        """Refresh AI context files"""
        print("🔄 Refreshing AI context...")

        try:
            from .context_extractor import ContextExtractor

            extractor = ContextExtractor(self.config)
            extractor.extract_and_generate_context()
            print("   ✅ AI context refreshed")
        except Exception as e:
            print(f"   ❌ Error refreshing context: {e}")

    def get_session_statistics(self) -> Dict[str, Any]:
        """Get statistics about recent sessions"""
        log_dir = self.config.get_session_log_directory()

        if not log_dir.exists():
            return {"total_sessions": 0, "recent_sessions": 0}

        log_files = list(log_dir.glob("session_*.md"))

        # Count recent sessions (last 30 days)
        recent_count = 0
        cutoff_date = datetime.now().timestamp() - (30 * 24 * 60 * 60)

        for log_file in log_files:
            if log_file.stat().st_mtime > cutoff_date:
                recent_count += 1

        return {
            "total_sessions": len(log_files),
            "recent_sessions": recent_count,
            "log_directory": str(log_dir),
        }
