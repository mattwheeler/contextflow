#!/usr/bin/env python3
"""
ContextFlow Demo Script
Demonstrates the core functionality of ContextFlow
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add the contextflow package to the path
sys.path.insert(0, str(Path(__file__).parent))

from contextflow.core.config import ContextFlowConfig
from contextflow.core.session_updater import SessionUpdater
from contextflow.core.context_extractor import ContextExtractor
from contextflow.templates.project_templates import ProjectTemplates

console = Console()


def demo_project_creation():
    """Demonstrate project creation from template"""
    console.print(Panel.fit(
        "ContextFlow Demo: Project Creation",
        style="bold blue"
    ))

    # Create a demo project
    templates = ProjectTemplates()

    console.print("Available Templates:")
    available = templates.get_available_templates()

    table = Table()
    table.add_column("Template", style="cyan")
    table.add_column("Description", style="white")

    for name, info in available.items():
        table.add_row(name, info['description'])

    console.print(table)

    # Create a side project
    console.print("\nCreating demo side project...")

    config = templates.create_project_from_template(
        'side-project',
        'ContextFlow Demo Project',
        'Demonstrating ContextFlow capabilities'
    )

    console.print("Demo project created!")
    return config


def demo_context_extraction(config):
    """Demonstrate AI context extraction"""
    console.print(Panel.fit(
        "🤖 ContextFlow Demo: AI Context Extraction",
        style="bold green"
    ))
    
    extractor = ContextExtractor(config)
    
    console.print("🔄 Extracting project context...")
    success = extractor.extract_and_generate_context()
    
    if success:
        console.print("✅ Context extraction complete!")
        
        # Show quick context
        context_dir = config.get_context_directory()
        quick_file = context_dir / config.ai_context.quick_context_file
        
        if quick_file.exists():
            console.print("\n📄 Generated Quick Context:")
            content = quick_file.read_text(encoding='utf-8')
            console.print(Panel(
                content[:500] + "..." if len(content) > 500 else content,
                title="Quick AI Context",
                border_style="green"
            ))
    else:
        console.print("❌ Context extraction failed")


def demo_session_update(config):
    """Demonstrate session documentation update"""
    console.print(Panel.fit(
        "📝 ContextFlow Demo: Session Documentation Update",
        style="bold yellow"
    ))
    
    updater = SessionUpdater(config)
    
    # Demo session summary
    demo_summary = """
Implemented user authentication system with JWT tokens in src/auth/jwt.py.
Added login and registration endpoints to src/api/auth.py.
Created React login component in src/components/Login.tsx.
Updated user stories PROJ-123 and PROJ-124.
Fixed responsive design issues in mobile navigation.
Added unit tests for authentication flow with 95% coverage.
"""
    
    console.print("🎯 Demo session summary:")
    console.print(Panel(demo_summary.strip(), border_style="yellow"))
    
    console.print("\n🔄 Processing session update...")
    success = updater.update_session_documentation(demo_summary)
    
    if success:
        console.print("✅ Session documentation updated!")
        
        # Show statistics
        stats = updater.get_session_statistics()
        console.print(f"\n📊 Session Statistics:")
        console.print(f"   Total sessions: {stats['total_sessions']}")
        console.print(f"   Recent sessions: {stats['recent_sessions']}")
    else:
        console.print("❌ Session update failed")


def demo_workflow_status(config):
    """Demonstrate workflow status and recommendations"""
    console.print(Panel.fit(
        "⚙️ ContextFlow Demo: Workflow Status",
        style="bold magenta"
    ))
    
    from contextflow.core.workflow_manager import WorkflowManager
    
    workflow = WorkflowManager(config)
    status = workflow.get_workflow_status()
    
    # Show configuration
    console.print("📋 Workflow Configuration:")
    config_table = Table()
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value", style="white")
    
    config_data = status['configuration']
    config_table.add_row("Mandatory Updates", "✅ Yes" if config_data['mandatory_updates'] else "❌ No")
    config_table.add_row("Require Work Items", "✅ Yes" if config_data['require_work_items'] else "❌ No")
    config_table.add_row("Auto Refresh", "✅ Yes" if config_data['auto_refresh'] else "❌ No")
    config_table.add_row("Retention Days", str(config_data['retention_days']))
    
    console.print(config_table)
    
    # Show recommendations
    recommendations = workflow.get_workflow_recommendations()
    if recommendations:
        console.print("\n💡 Workflow Recommendations:")
        for rec in recommendations:
            console.print(f"   • {rec}")


def demo_integration_status(config):
    """Demonstrate integration status"""
    console.print(Panel.fit(
        "🔗 ContextFlow Demo: Integration Status",
        style="bold cyan"
    ))
    
    integrations_table = Table()
    integrations_table.add_column("Integration", style="cyan")
    integrations_table.add_column("Status", style="white")
    integrations_table.add_column("Configuration", style="yellow")
    
    for integration in ['confluence', 'jira', 'github', 'notion', 'slack']:
        enabled = config.is_integration_enabled(integration)
        status = "✅ Enabled" if enabled else "❌ Disabled"
        
        if enabled:
            int_config = config.get_integration_config(integration)
            config_info = f"{len(int_config)} settings configured"
        else:
            config_info = "Not configured"
        
        integrations_table.add_row(integration.title(), status, config_info)
    
    console.print(integrations_table)


def main():
    """Run the complete ContextFlow demo"""
    console.print(Panel.fit(
        "ContextFlow - AI Session Context & Workflow Automation\n"
        "Never lose context between AI sessions again!",
        style="bold blue",
        title="Welcome to ContextFlow Demo"
    ))
    
    try:
        # Change to a temporary directory for demo
        demo_dir = Path("/tmp/contextflow-demo")
        demo_dir.mkdir(exist_ok=True)
        os.chdir(demo_dir)
        
        # Demo 1: Project Creation
        config = demo_project_creation()
        
        console.print("\n" + "="*60 + "\n")
        
        # Demo 2: Context Extraction
        demo_context_extraction(config)
        
        console.print("\n" + "="*60 + "\n")
        
        # Demo 3: Session Update
        demo_session_update(config)
        
        console.print("\n" + "="*60 + "\n")
        
        # Demo 4: Workflow Status
        demo_workflow_status(config)
        
        console.print("\n" + "="*60 + "\n")
        
        # Demo 5: Integration Status
        demo_integration_status(config)
        
        console.print("\n" + "="*60 + "\n")
        
        # Final summary
        console.print(Panel.fit(
            "🎉 ContextFlow Demo Complete!\n\n"
            "Key Features Demonstrated:\n"
            "✅ Project templates and initialization\n"
            "✅ AI context extraction and formatting\n"
            "✅ Session documentation automation\n"
            "✅ Workflow management and validation\n"
            "✅ Multi-platform integrations\n\n"
            "Ready to transform your AI-assisted workflow!",
            style="bold green",
            title="Demo Summary"
        ))
        
        console.print(f"\n📁 Demo files created in: {demo_dir}")
        console.print("🚀 Try ContextFlow in your own projects!")
        
    except Exception as e:
        console.print(f"❌ Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
