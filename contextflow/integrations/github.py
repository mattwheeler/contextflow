"""
ContextFlow GitHub Integration
"""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime


class GitHubIntegration:
    """GitHub integration for ContextFlow with secure credential handling"""

    def __init__(self, config: Dict[str, Any], contextflow_config=None):
        self.config = config
        self.contextflow_config = contextflow_config
        self.repository = config.get("repository", "")

        # Get credentials securely
        if contextflow_config:
            credentials = contextflow_config.get_integration_credentials("github")
            self.token = credentials.get("token", "")
        else:
            # Fallback to config (for backward compatibility)
            self.token = config.get("token", "")

        if self.token:
            self.headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
            }
        else:
            self.headers = {}
            print("GitHub token not configured. Run: contextflow setup github")

    def update_from_session(self, session_updates: Dict[str, Any]):
        """Update GitHub based on session updates"""
        if not self.token:
            print("   ⚠️  GitHub: No token configured")
            return

        work_items = session_updates.get("work_items", [])

        if not work_items:
            print("   ℹ️  GitHub: No work items to update")
            return

        try:
            for work_item in work_items:
                if self._is_github_issue(work_item):
                    issue_number = self._extract_issue_number(work_item)
                    if issue_number:
                        self._add_session_comment(issue_number, session_updates)

            print(f"   ✅ GitHub updated for relevant work items")

        except Exception as e:
            print(f"   ❌ GitHub update failed: {e}")

    def _is_github_issue(self, work_item: str) -> bool:
        """Check if work item is a GitHub issue format"""
        import re

        # Match patterns like #123, issue-456, etc.
        return bool(re.match(r"^#?\d+$", work_item) or re.match(r"^issue-\d+$", work_item))

    def _extract_issue_number(self, work_item: str) -> Optional[int]:
        """Extract issue number from work item"""
        import re

        # Handle #123 format
        match = re.match(r"^#?(\d+)$", work_item)
        if match:
            return int(match.group(1))

        # Handle issue-123 format
        match = re.match(r"^issue-(\d+)$", work_item)
        if match:
            return int(match.group(1))

        return None

    def _add_session_comment(self, issue_number: int, session_updates: Dict[str, Any]):
        """Add session comment to GitHub issue"""
        try:
            url = f"https://api.github.com/repos/{self.repository}/issues/{issue_number}/comments"

            # Format comment content
            comment_body = self._format_session_comment(session_updates)

            comment_data = {"body": comment_body}

            response = requests.post(url, json=comment_data, headers=self.headers)

            if response.status_code == 201:
                print(f"   ✅ Comment added to issue #{issue_number}")
            else:
                print(f"   ❌ Failed to comment on issue #{issue_number}: {response.status_code}")

        except Exception as e:
            print(f"   ❌ Error commenting on issue #{issue_number}: {e}")

    def _format_session_comment(self, session_updates: Dict[str, Any]) -> str:
        """Format session updates for GitHub comment"""
        summary = session_updates.get("summary", "No summary provided")
        categories = session_updates.get("categories", [])
        files_changed = session_updates.get("files_changed", [])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        comment = f"## 🤖 ContextFlow Session Update - {timestamp}\n\n"
        comment += f"**Summary:** {summary}\n\n"

        if categories:
            comment += f"**Categories:** {', '.join(categories)}\n\n"

        if files_changed:
            comment += f"**Files Modified:** {len(files_changed)} files\n"
            if len(files_changed) <= 10:
                comment += "```\n"
                for file in files_changed:
                    comment += f"- {file}\n"
                comment += "```\n"
            comment += "\n"

        comment += "---\n*Updated via ContextFlow automation*"

        return comment

    def get_repository_issues(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent issues from the repository"""
        if not self.token:
            return []

        try:
            url = f"https://api.github.com/repos/{self.repository}/issues"

            params = {"state": "open", "sort": "updated", "direction": "desc", "per_page": limit}

            response = requests.get(url, params=params, headers=self.headers)

            if response.status_code == 200:
                issues_data = response.json()
                issues = []

                for issue in issues_data:
                    # Skip pull requests (they appear as issues in GitHub API)
                    if "pull_request" not in issue:
                        issues.append(
                            {
                                "number": issue["number"],
                                "title": issue["title"],
                                "state": issue["state"],
                                "assignee": issue["assignee"]["login"]
                                if issue["assignee"]
                                else "Unassigned",
                                "updated_at": issue["updated_at"],
                                "url": issue["html_url"],
                            }
                        )

                return issues

            return []

        except Exception as e:
            print(f"   ⚠️  Error getting GitHub issues: {e}")
            return []

    def get_recent_commits(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commits from the repository"""
        if not self.token:
            return []

        try:
            url = f"https://api.github.com/repos/{self.repository}/commits"

            params = {"per_page": limit}

            response = requests.get(url, params=params, headers=self.headers)

            if response.status_code == 200:
                commits_data = response.json()
                commits = []

                for commit in commits_data:
                    commits.append(
                        {
                            "sha": commit["sha"][:7],
                            "message": commit["commit"]["message"].split("\n")[
                                0
                            ],  # First line only
                            "author": commit["commit"]["author"]["name"],
                            "date": commit["commit"]["author"]["date"],
                            "url": commit["html_url"],
                        }
                    )

                return commits

            return []

        except Exception as e:
            print(f"   ⚠️  Error getting GitHub commits: {e}")
            return []

    def extract_project_context(self) -> Dict[str, Any]:
        """Extract project context from GitHub"""
        if not self.token:
            return {}

        try:
            # Get repository info
            repo_info = self._get_repository_info()

            # Get recent issues and commits
            issues = self.get_repository_issues(5)
            commits = self.get_recent_commits(5)

            return {
                "github_repository": {
                    "name": self.repository,
                    "description": repo_info.get("description", ""),
                    "url": f"https://github.com/{self.repository}",
                    "language": repo_info.get("language", "Unknown"),
                },
                "recent_issues": issues,
                "recent_commits": commits,
            }

        except Exception as e:
            print(f"   ⚠️  Error extracting GitHub context: {e}")
            return {}

    def _get_repository_info(self) -> Dict[str, Any]:
        """Get repository information"""
        try:
            url = f"https://api.github.com/repos/{self.repository}"

            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                return response.json()

            return {}

        except Exception as e:
            print(f"   ⚠️  Error getting repository info: {e}")
            return {}
