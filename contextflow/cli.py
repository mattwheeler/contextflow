"""
ContextFlow Command Line Interface
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .core.config import ContextFlowConfig
from .core.session_updater import SessionUpdater
from .core.context_extractor import ContextExtractor
from .templates.project_templates import ProjectTemplates

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    ContextFlow - AI Session Context & Workflow Automation

    Never lose context between AI sessions again.
    """
    pass


@main.command()
@click.option('--template', '-t', default='software-development', 
              help='Project template to use')
@click.option('--name', '-n', prompt='Project name', 
              help='Name of the project')
@click.option('--description', '-d', prompt='Project description', 
              help='Description of the project')
def init(template, name, description):
    """Initialize a new ContextFlow project"""
    try:
        console.print(f"Initializing ContextFlow project: [bold]{name}[/bold]")

        # Create project configuration
        templates = ProjectTemplates()
        config = templates.create_project_from_template(template, name, description)

        if config:
            console.print(f"Project initialized with template: [bold]{template}[/bold]")
            console.print(f"Configuration saved to: [bold]contextflow.yaml[/bold]")

            # Generate initial context
            extractor = ContextExtractor(config)
            extractor.extract_and_generate_context()

            console.print("\nNext steps:")
            console.print("1. Review and customize contextflow.yaml")
            console.print("2. Configure your integrations (JIRA, Confluence, etc.)")
            console.print("3. Start your first session with: contextflow context")
        else:
            console.print("Failed to initialize project")
            sys.exit(1)

    except Exception as e:
        console.print(f"Error initializing project: {e}")
        sys.exit(1)


@main.command()
@click.option('--quick', '-q', is_flag=True, 
              help='Show quick context for immediate use')
@click.option('--refresh', '-r', is_flag=True, 
              help='Refresh context from latest project state')
def context(quick, refresh):
    """Get AI context for new sessions"""
    try:
        config = ContextFlowConfig()

        if refresh:
            console.print("Refreshing AI context...")
            extractor = ContextExtractor(config)
            extractor.extract_and_generate_context()

        context_dir = config.get_context_directory()

        if quick:
            quick_file = context_dir / config.ai_context.quick_context_file
            if quick_file.exists():
                console.print(Panel.fit(
                    quick_file.read_text(encoding='utf-8'),
                    title="Quick AI Context",
                    border_style="green"
                ))
                console.print("\nCopy the above content and paste into your new AI session")
            else:
                console.print("Quick context file not found. Run: contextflow context --refresh")
        else:
            full_file = context_dir / config.ai_context.full_context_file
            if full_file.exists():
                console.print(f"Full context available at: [bold]{full_file}[/bold]")
                console.print("Use --quick flag for copy-paste ready context")
            else:
                console.print("Context files not found. Run: contextflow context --refresh")

    except Exception as e:
        console.print(f"Error getting context: {e}")
        sys.exit(1)


@main.command()
@click.argument('summary', required=True)
def update(summary):
    """Update session documentation"""
    try:
        config = ContextFlowConfig()
        
        if config.workflow.mandatory_session_updates:
            console.print("🔄 Updating session documentation...")
            
            updater = SessionUpdater(config)
            success = updater.update_session_documentation(summary)
            
            if success:
                console.print("✅ Session documentation updated successfully!")
                
                # Show statistics
                stats = updater.get_session_statistics()
                console.print(f"📊 Total sessions: {stats['total_sessions']}")
                console.print(f"📊 Recent sessions (30 days): {stats['recent_sessions']}")
            else:
                console.print("❌ Session documentation update failed")
                sys.exit(1)
        else:
            console.print("⚠️  Session updates are not mandatory for this project")
            console.print("💡 Enable with: mandatory_session_updates: true in contextflow.yaml")
            
    except Exception as e:
        console.print(f"❌ Error updating session: {e}")
        sys.exit(1)


@main.command()
@click.option('--recent', '-r', is_flag=True, 
              help='Show only recent session logs')
@click.option('--count', '-c', default=10, 
              help='Number of logs to show')
def logs(recent, count):
    """View session logs"""
    try:
        config = ContextFlowConfig()
        log_dir = config.get_session_log_directory()
        
        if not log_dir.exists():
            console.print("📝 No session logs found")
            return
        
        log_files = list(log_dir.glob("session_*.md"))
        
        if not log_files:
            console.print("📝 No session logs found")
            return
        
        # Sort by modification time (newest first)
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if recent:
            # Filter to recent logs (last 7 days)
            import time
            cutoff_time = time.time() - (7 * 24 * 60 * 60)
            log_files = [f for f in log_files if f.stat().st_mtime > cutoff_time]
        
        # Limit count
        log_files = log_files[:count]
        
        table = Table(title="📝 Session Logs")
        table.add_column("Date", style="cyan")
        table.add_column("Summary", style="white")
        
        for log_file in log_files:
            try:
                # Extract date from filename
                date_str = log_file.stem.replace('session_', '')
                date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {date_str[9:11]}:{date_str[11:13]}"
                
                # Extract summary from file
                content = log_file.read_text(encoding='utf-8')
                import re
                summary_match = re.search(r'## Session Summary\n\n(.*?)\n\n', content, re.DOTALL)
                summary = summary_match.group(1).strip()[:80] + "..." if summary_match else "No summary"
                
                table.add_row(date_formatted, summary)
            except Exception:
                table.add_row(log_file.name, "Error reading log")
        
        console.print(table)
        console.print(f"\n📁 Log directory: [bold]{log_dir}[/bold]")
        
    except Exception as e:
        console.print(f"❌ Error viewing logs: {e}")
        sys.exit(1)


@main.command()
def status():
    """Show project status and configuration"""
    try:
        config = ContextFlowConfig()
        
        # Project info
        console.print(Panel.fit(
            f"[bold]{config.project.name}[/bold]\n"
            f"Type: {config.project.type}\n"
            f"Version: {config.project.version}\n"
            f"Description: {config.project.description}",
            title="📁 Project Information",
            border_style="blue"
        ))
        
        # Integrations
        integrations_table = Table(title="🔗 Integrations")
        integrations_table.add_column("Integration", style="cyan")
        integrations_table.add_column("Status", style="white")
        
        for integration in ['confluence', 'jira', 'github', 'notion', 'slack']:
            status = "✅ Enabled" if config.is_integration_enabled(integration) else "❌ Disabled"
            integrations_table.add_row(integration.title(), status)
        
        console.print(integrations_table)
        
        # Workflow settings
        console.print(Panel.fit(
            f"Mandatory Updates: {'✅ Yes' if config.workflow.mandatory_session_updates else '❌ No'}\n"
            f"Work Item References: {'✅ Required' if config.workflow.require_work_item_references else '❌ Optional'}\n"
            f"Auto Refresh Context: {'✅ Yes' if config.ai_context.auto_refresh else '❌ No'}\n"
            f"Session Log Retention: {config.workflow.session_log_retention_days} days",
            title="⚙️ Workflow Configuration",
            border_style="green"
        ))
        
        # File locations
        console.print(Panel.fit(
            f"Context Directory: {config.get_context_directory()}\n"
            f"Session Logs: {config.get_session_log_directory()}\n"
            f"Config File: {config.config_path or 'Not found'}",
            title="📁 File Locations",
            border_style="yellow"
        ))
        
        # Session statistics
        updater = SessionUpdater(config)
        stats = updater.get_session_statistics()
        
        console.print(Panel.fit(
            f"Total Sessions: {stats['total_sessions']}\n"
            f"Recent Sessions (30 days): {stats['recent_sessions']}",
            title="📊 Session Statistics",
            border_style="magenta"
        ))
        
    except Exception as e:
        console.print(f"❌ Error getting status: {e}")
        sys.exit(1)


@main.command()
def templates():
    """List available project templates"""
    try:
        templates = ProjectTemplates()
        available_templates = templates.get_available_templates()

        table = Table(title="Available Project Templates")
        table.add_column("Template", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Integrations", style="green")

        for template_name, template_info in available_templates.items():
            integrations = ", ".join(template_info.get('integrations', []))
            table.add_row(
                template_name,
                template_info.get('description', 'No description'),
                integrations
            )

        console.print(table)
        console.print("\nUse: contextflow init --template <template-name>")

    except Exception as e:
        console.print(f"Error listing templates: {e}")
        sys.exit(1)


@main.command()
@click.argument('integration', required=True)
def setup(integration):
    """Setup credentials for an integration"""
    try:
        config = ContextFlowConfig()

        valid_integrations = ['confluence', 'jira', 'github', 'notion', 'slack']

        if integration not in valid_integrations:
            console.print(f"Invalid integration: {integration}")
            console.print(f"Valid options: {', '.join(valid_integrations)}")
            sys.exit(1)

        console.print(f"Setting up {integration.title()} integration...")
        config.setup_integration_credentials(integration)

    except Exception as e:
        console.print(f"Error setting up {integration}: {e}")
        sys.exit(1)


@main.command()
def credentials():
    """List stored credentials"""
    try:
        config = ContextFlowConfig()
        stored = config.list_stored_credentials()

        if not stored:
            console.print("No credentials stored.")
            console.print("Use 'contextflow setup <integration>' to add credentials.")
            return

        table = Table(title="Stored Credentials")
        table.add_column("Integration", style="cyan")
        table.add_column("Credentials", style="green")

        for integration, creds in stored.items():
            table.add_row(integration.title(), ", ".join(creds))

        console.print(table)
        console.print("\nCredentials are stored securely using your system's keyring.")

    except Exception as e:
        console.print(f"Error listing credentials: {e}")
        sys.exit(1)


@main.command()
@click.argument('integration', required=True)
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def remove_credentials(integration, confirm):
    """Remove stored credentials for an integration"""
    try:
        config = ContextFlowConfig()

        if not confirm:
            response = input(f"Remove all credentials for {integration}? (y/N): ")
            if response.lower() != 'y':
                console.print("Cancelled.")
                return

        config.remove_credentials(integration)

    except Exception as e:
        console.print(f"Error removing credentials: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
