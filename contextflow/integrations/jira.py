"""
ContextFlow JIRA Integration
"""

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, Optional, List
from datetime import datetime


class JiraIntegration:
    """JIRA integration for ContextFlow with secure credential handling"""

    def __init__(self, config: Dict[str, Any], contextflow_config=None):
        self.config = config
        self.contextflow_config = contextflow_config
        self.base_url = config.get('base_url', '')
        self.project_key = config.get('project_key', '')

        # Get credentials securely
        if contextflow_config:
            credentials = contextflow_config.get_integration_credentials('jira')
            self.username = credentials.get('username', '')
            self.api_token = credentials.get('api_token', '')
        else:
            # Fallback to config (for backward compatibility)
            self.username = config.get('username', '')
            self.api_token = config.get('api_token', '')

        if self.username and self.api_token:
            self.auth = HTTPBasicAuth(self.username, self.api_token)
        else:
            self.auth = None
            print("JIRA credentials not configured. Run: contextflow setup jira")
    
    def update_from_session(self, session_updates: Dict[str, Any]):
        """Update JIRA based on session updates"""
        if not self.auth:
            print("   ⚠️  JIRA: No authentication configured")
            return
        
        work_items = session_updates.get('work_items', [])
        
        if not work_items:
            print("   ℹ️  JIRA: No work items to update")
            return
        
        try:
            for work_item in work_items:
                if self._is_jira_issue(work_item):
                    self._add_session_comment(work_item, session_updates)
            
            print(f"   ✅ JIRA updated for {len(work_items)} work items")
            
        except Exception as e:
            print(f"   ❌ JIRA update failed: {e}")
    
    def _is_jira_issue(self, work_item: str) -> bool:
        """Check if work item is a JIRA issue format"""
        import re
        # Match patterns like PROJ-123, ABC-456, etc.
        return bool(re.match(r'^[A-Z]+-\d+$', work_item))
    
    def _add_session_comment(self, issue_key: str, session_updates: Dict[str, Any]):
        """Add session comment to JIRA issue"""
        try:
            url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
            
            # Format comment content
            comment_body = self._format_session_comment(session_updates)
            
            comment_data = {
                "body": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"🤖 ContextFlow Session Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                                }
                            ]
                        },
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": comment_body
                                }
                            ]
                        }
                    ]
                }
            }
            
            response = requests.post(url, json=comment_data, auth=self.auth)
            
            if response.status_code == 201:
                print(f"   ✅ Comment added to {issue_key}")
            else:
                print(f"   ❌ Failed to comment on {issue_key}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error commenting on {issue_key}: {e}")
    
    def _format_session_comment(self, session_updates: Dict[str, Any]) -> str:
        """Format session updates for JIRA comment"""
        summary = session_updates.get('summary', 'No summary provided')
        categories = session_updates.get('categories', [])
        files_changed = session_updates.get('files_changed', [])
        
        comment = f"Session Summary: {summary}"
        
        if categories:
            comment += f"\n\nCategories: {', '.join(categories)}"
        
        if files_changed:
            comment += f"\n\nFiles Modified: {len(files_changed)} files"
            if len(files_changed) <= 5:
                comment += f" ({', '.join(files_changed)})"
        
        comment += "\n\n---\nUpdated via ContextFlow automation"
        
        return comment
    
    def get_project_issues(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent issues from the project"""
        if not self.auth:
            return []
        
        try:
            url = f"{self.base_url}/rest/api/3/search"
            
            jql = f"project = {self.project_key} ORDER BY updated DESC"
            
            params = {
                'jql': jql,
                'maxResults': limit,
                'fields': 'summary,status,assignee,updated'
            }
            
            response = requests.get(url, params=params, auth=self.auth)
            
            if response.status_code == 200:
                data = response.json()
                issues = []
                
                for issue in data['issues']:
                    issues.append({
                        'key': issue['key'],
                        'summary': issue['fields']['summary'],
                        'status': issue['fields']['status']['name'],
                        'assignee': issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else 'Unassigned',
                        'updated': issue['fields']['updated']
                    })
                
                return issues
            
            return []
            
        except Exception as e:
            print(f"   ⚠️  Error getting JIRA issues: {e}")
            return []
    
    def extract_project_context(self) -> Dict[str, Any]:
        """Extract project context from JIRA"""
        if not self.auth:
            return {}
        
        try:
            # Get recent issues
            issues = self.get_project_issues(10)
            
            # Get project info
            project_info = self._get_project_info()
            
            return {
                'jira_project': {
                    'key': self.project_key,
                    'name': project_info.get('name', self.project_key),
                    'url': f"{self.base_url}/browse/{self.project_key}"
                },
                'recent_issues': issues
            }
            
        except Exception as e:
            print(f"   ⚠️  Error extracting JIRA context: {e}")
            return {}
    
    def _get_project_info(self) -> Dict[str, Any]:
        """Get project information"""
        try:
            url = f"{self.base_url}/rest/api/3/project/{self.project_key}"
            
            response = requests.get(url, auth=self.auth)
            
            if response.status_code == 200:
                return response.json()
            
            return {}
            
        except Exception as e:
            print(f"   ⚠️  Error getting project info: {e}")
            return {}
