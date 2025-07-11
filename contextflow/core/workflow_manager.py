"""
ContextFlow Workflow Manager
Manages workflow automation and validation
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from .config import ContextFlowConfig


class WorkflowManager:
    """Manage workflow automation and validation"""

    def __init__(self, config: Optional[ContextFlowConfig] = None):
        self.config = config or ContextFlowConfig()

    def validate_session_update(self, session_summary: str) -> Dict[str, Any]:
        """Validate session update against workflow requirements"""
        validation = {"valid": True, "warnings": [], "errors": [], "suggestions": []}

        # Check if work item references are required
        if self.config.workflow.require_work_item_references:
            if not self._has_work_item_references(session_summary):
                validation["errors"].append(
                    "Work item references are required but none found. "
                    "Include references like PROJ-123, #456, or issue-789."
                )
                validation["valid"] = False

        # Check for minimum content
        if len(session_summary.strip()) < 20:
            validation["warnings"].append(
                "Session summary is very short. Consider adding more detail about what was accomplished."
            )

        # Check for common patterns
        if not self._has_action_words(session_summary):
            validation["suggestions"].append(
                "Consider including action words like 'implemented', 'fixed', 'added', 'updated' to clarify what was done."
            )

        # Check for file references
        if not self._has_file_references(session_summary):
            validation["suggestions"].append(
                "Consider mentioning specific files that were modified to help track changes."
            )

        return validation

    def _has_work_item_references(self, text: str) -> bool:
        """Check if text contains work item references"""
        import re

        patterns = [
            r"[A-Z]+-\d+",  # JIRA-style
            r"#\d+",  # GitHub-style
            r"issue-\d+",  # Generic issue
            r"task-\d+",  # Generic task
        ]

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    def _has_action_words(self, text: str) -> bool:
        """Check if text contains action words"""
        action_words = [
            "implemented",
            "added",
            "created",
            "built",
            "developed",
            "fixed",
            "resolved",
            "corrected",
            "repaired",
            "updated",
            "modified",
            "changed",
            "improved",
            "refactored",
            "optimized",
            "enhanced",
            "tested",
            "validated",
            "verified",
            "documented",
            "wrote",
            "drafted",
        ]

        text_lower = text.lower()
        return any(word in text_lower for word in action_words)

    def _has_file_references(self, text: str) -> bool:
        """Check if text contains file references"""
        import re

        # Look for file paths or extensions
        file_patterns = [
            r"\w+\.\w+",  # filename.ext
            r"src/\w+",  # src/file
            r"lib/\w+",  # lib/file
            r"components/\w+",  # components/file
            r"pages/\w+",  # pages/file
        ]

        for pattern in file_patterns:
            if re.search(pattern, text):
                return True

        return False

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status and statistics"""
        status = {
            "configuration": {
                "mandatory_updates": self.config.workflow.mandatory_session_updates,
                "require_work_items": self.config.workflow.require_work_item_references,
                "auto_refresh": self.config.ai_context.auto_refresh,
                "retention_days": self.config.workflow.session_log_retention_days,
            },
            "session_statistics": self._get_session_statistics(),
            "maintenance": self._get_maintenance_status(),
        }

        return status

    def _get_session_statistics(self) -> Dict[str, Any]:
        """Get session statistics"""
        log_dir = self.config.get_session_log_directory()

        if not log_dir.exists():
            return {
                "total_sessions": 0,
                "recent_sessions": 0,
                "avg_sessions_per_week": 0,
                "last_session": None,
            }

        log_files = list(log_dir.glob("session_*.md"))

        if not log_files:
            return {
                "total_sessions": 0,
                "recent_sessions": 0,
                "avg_sessions_per_week": 0,
                "last_session": None,
            }

        # Sort by modification time
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # Count recent sessions (last 30 days)
        recent_cutoff = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        recent_sessions = sum(1 for f in log_files if f.stat().st_mtime > recent_cutoff)

        # Calculate average sessions per week (last 8 weeks)
        week_cutoff = datetime.now().timestamp() - (8 * 7 * 24 * 60 * 60)
        weekly_sessions = sum(1 for f in log_files if f.stat().st_mtime > week_cutoff)
        avg_per_week = weekly_sessions / 8 if weekly_sessions > 0 else 0

        # Get last session date
        last_session = None
        if log_files:
            last_session = datetime.fromtimestamp(log_files[0].stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M"
            )

        return {
            "total_sessions": len(log_files),
            "recent_sessions": recent_sessions,
            "avg_sessions_per_week": round(avg_per_week, 1),
            "last_session": last_session,
        }

    def _get_maintenance_status(self) -> Dict[str, Any]:
        """Get maintenance status"""
        log_dir = self.config.get_session_log_directory()
        context_dir = self.config.get_context_directory()

        maintenance = {
            "log_cleanup_needed": False,
            "context_refresh_needed": False,
            "old_logs_count": 0,
            "context_age_days": 0,
        }

        # Check if log cleanup is needed
        if log_dir.exists():
            retention_cutoff = datetime.now().timestamp() - (
                self.config.workflow.session_log_retention_days * 24 * 60 * 60
            )
            old_logs = [
                f for f in log_dir.glob("session_*.md") if f.stat().st_mtime < retention_cutoff
            ]

            maintenance["old_logs_count"] = len(old_logs)
            maintenance["log_cleanup_needed"] = len(old_logs) > 0

        # Check if context refresh is needed
        quick_context_file = context_dir / self.config.ai_context.quick_context_file
        if quick_context_file.exists():
            context_age = datetime.now().timestamp() - quick_context_file.stat().st_mtime
            context_age_days = context_age / (24 * 60 * 60)

            maintenance["context_age_days"] = round(context_age_days, 1)
            maintenance["context_refresh_needed"] = (
                context_age_days > 7
            )  # Refresh if older than 7 days
        else:
            maintenance["context_refresh_needed"] = True

        return maintenance

    def cleanup_old_logs(self) -> Dict[str, Any]:
        """Clean up old session logs"""
        log_dir = self.config.get_session_log_directory()

        if not log_dir.exists():
            return {"cleaned": 0, "archived": 0, "errors": []}

        retention_cutoff = datetime.now().timestamp() - (
            self.config.workflow.session_log_retention_days * 24 * 60 * 60
        )
        old_logs = [f for f in log_dir.glob("session_*.md") if f.stat().st_mtime < retention_cutoff]

        if not old_logs:
            return {"cleaned": 0, "archived": 0, "errors": []}

        # Create archive directory
        archive_dir = log_dir / "archive" / datetime.now().strftime("%Y-%m")
        archive_dir.mkdir(parents=True, exist_ok=True)

        cleaned = 0
        archived = 0
        errors = []

        for log_file in old_logs:
            try:
                if self.config.workflow.auto_archive_logs:
                    # Move to archive
                    archive_path = archive_dir / log_file.name
                    log_file.rename(archive_path)
                    archived += 1
                else:
                    # Delete permanently
                    log_file.unlink()
                    cleaned += 1
            except Exception as e:
                errors.append(f"Error processing {log_file.name}: {e}")

        return {"cleaned": cleaned, "archived": archived, "errors": errors}

    def enforce_workflow_compliance(self, session_summary: str) -> bool:
        """Enforce workflow compliance before allowing session update"""
        if not self.config.workflow.mandatory_session_updates:
            return True

        validation = self.validate_session_update(session_summary)

        if not validation["valid"]:
            print("❌ Session update validation failed:")
            for error in validation["errors"]:
                print(f"   • {error}")
            return False

        if validation["warnings"]:
            print("⚠️  Session update warnings:")
            for warning in validation["warnings"]:
                print(f"   • {warning}")

        if validation["suggestions"]:
            print("💡 Session update suggestions:")
            for suggestion in validation["suggestions"]:
                print(f"   • {suggestion}")

        return True

    def get_workflow_recommendations(self) -> List[str]:
        """Get workflow improvement recommendations"""
        recommendations = []

        stats = self._get_session_statistics()
        maintenance = self._get_maintenance_status()

        # Session frequency recommendations
        if stats["avg_sessions_per_week"] < 2:
            recommendations.append(
                "Consider more frequent session updates (2-3 per week) for better project continuity."
            )
        elif stats["avg_sessions_per_week"] > 10:
            recommendations.append(
                "Very high session frequency detected. Consider consolidating smaller updates."
            )

        # Maintenance recommendations
        if maintenance["log_cleanup_needed"]:
            recommendations.append(
                f"Clean up {maintenance['old_logs_count']} old session logs to maintain performance."
            )

        if maintenance["context_refresh_needed"]:
            recommendations.append(
                f"Refresh AI context (last updated {maintenance['context_age_days']} days ago)."
            )

        # Configuration recommendations
        if not self.config.workflow.mandatory_session_updates:
            recommendations.append("Enable mandatory session updates for better project tracking.")

        if not self.config.workflow.require_work_item_references:
            recommendations.append(
                "Consider requiring work item references to improve traceability."
            )

        return recommendations
