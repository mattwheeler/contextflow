"""
ContextFlow Confluence Integration
"""

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, Optional
from datetime import datetime


class ConfluenceIntegration:
    """Confluence integration for ContextFlow with secure credential handling"""

    def __init__(self, config: Dict[str, Any], contextflow_config=None):
        self.config = config
        self.contextflow_config = contextflow_config
        self.base_url = config.get("base_url", "")
        self.space_key = config.get("space_key", "")

        # Get credentials securely
        if contextflow_config:
            credentials = contextflow_config.get_integration_credentials("confluence")
            self.username = credentials.get("username", "")
            self.api_token = credentials.get("api_token", "")
        else:
            # Fallback to config (for backward compatibility)
            self.username = config.get("username", "")
            self.api_token = config.get("api_token", "")

        if self.username and self.api_token:
            self.auth = HTTPBasicAuth(self.username, self.api_token)
        else:
            self.auth = None
            print("Confluence credentials not configured. Run: contextflow setup confluence")

    def update_from_session(self, session_updates: Dict[str, Any]):
        """Update Confluence based on session updates"""
        if not self.auth:
            print("   ⚠️  Confluence: No authentication configured")
            return

        try:
            # Find or create session updates page
            page_id = self._find_or_create_session_page()

            if page_id:
                self._add_session_update(page_id, session_updates)
                print("   ✅ Confluence updated with session information")
            else:
                print("   ❌ Confluence: Could not find or create session page")

        except Exception as e:
            print(f"   ❌ Confluence update failed: {e}")

    def _find_or_create_session_page(self) -> Optional[str]:
        """Find or create a page for session updates"""
        page_title = "ContextFlow Session Updates"

        # Try to find existing page
        try:
            url = f"{self.base_url}/wiki/rest/api/content"
            params = {"spaceKey": self.space_key, "title": page_title, "type": "page"}

            response = requests.get(url, params=params, auth=self.auth)

            if response.status_code == 200:
                data = response.json()
                if data["results"]:
                    return data["results"][0]["id"]

            # Create new page if not found
            return self._create_session_page(page_title)

        except Exception as e:
            print(f"   ❌ Error finding Confluence page: {e}")
            return None

    def _create_session_page(self, title: str) -> Optional[str]:
        """Create a new session updates page"""
        try:
            url = f"{self.base_url}/wiki/rest/api/content"

            page_data = {
                "type": "page",
                "title": title,
                "space": {"key": self.space_key},
                "body": {
                    "storage": {
                        "value": f"""
<h1>ContextFlow Session Updates</h1>
<p>This page tracks all ContextFlow session updates for the project.</p>
<p><em>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
<hr/>
""",
                        "representation": "storage",
                    }
                },
            }

            response = requests.post(url, json=page_data, auth=self.auth)

            if response.status_code == 200:
                page_info = response.json()
                return page_info["id"]
            else:
                print(f"   ❌ Failed to create Confluence page: {response.status_code}")
                return None

        except Exception as e:
            print(f"   ❌ Error creating Confluence page: {e}")
            return None

    def _add_session_update(self, page_id: str, session_updates: Dict[str, Any]):
        """Add session update to existing page"""
        try:
            # Get current page content
            url = f"{self.base_url}/wiki/rest/api/content/{page_id}"
            params = {"expand": "body.storage,version"}

            response = requests.get(url, params=params, auth=self.auth)

            if response.status_code == 200:
                page_data = response.json()
                current_content = page_data["body"]["storage"]["value"]
                current_version = page_data["version"]["number"]

                # Create session update content
                update_content = self._format_session_update(session_updates)

                # Prepend new update to existing content
                new_content = current_content.replace("<hr/>", f"{update_content}<hr/>")

                # Update the page
                update_data = {
                    "version": {"number": current_version + 1},
                    "title": page_data["title"],
                    "type": "page",
                    "body": {"storage": {"value": new_content, "representation": "storage"}},
                }

                update_response = requests.put(url, json=update_data, auth=self.auth)
                return update_response.status_code == 200

            return False

        except Exception as e:
            print(f"   ❌ Error updating Confluence page: {e}")
            return False

    def _format_session_update(self, session_updates: Dict[str, Any]) -> str:
        """Format session updates for Confluence"""
        timestamp = session_updates.get("timestamp", datetime.now().isoformat())
        summary = session_updates.get("summary", "No summary provided")
        categories = session_updates.get("categories", [])
        work_items = session_updates.get("work_items", [])
        files_changed = session_updates.get("files_changed", [])

        content = f"""
<h2>🔄 Session Update - {datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M')}</h2>
<p><strong>Summary:</strong> {summary}</p>
"""

        if categories:
            content += f"<p><strong>Categories:</strong> {', '.join(categories)}</p>"

        if work_items:
            content += "<p><strong>Work Items:</strong></p><ul>"
            for item in work_items:
                content += f"<li>{item}</li>"
            content += "</ul>"

        if files_changed:
            content += "<p><strong>Files Changed:</strong></p><ul>"
            for file in files_changed[:10]:  # Limit to first 10 files
                content += f"<li><code>{file}</code></li>"
            content += "</ul>"

        content += f"<p><em>Updated by ContextFlow at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>"

        return content

    def extract_project_context(self) -> Dict[str, Any]:
        """Extract project context from Confluence"""
        if not self.auth:
            return {}

        try:
            # Get pages from the space
            url = f"{self.base_url}/wiki/rest/api/content"
            params = {"spaceKey": self.space_key, "type": "page", "limit": 10}

            response = requests.get(url, params=params, auth=self.auth)

            if response.status_code == 200:
                data = response.json()
                pages = []

                for page in data["results"]:
                    pages.append(
                        {
                            "title": page["title"],
                            "url": f"{self.base_url}/wiki{page['_links']['webui']}",
                        }
                    )

                return {
                    "confluence_pages": pages,
                    "space_key": self.space_key,
                    "space_url": f"{self.base_url}/wiki/spaces/{self.space_key}",
                }

            return {}

        except Exception as e:
            print(f"   ⚠️  Error extracting Confluence context: {e}")
            return {}
