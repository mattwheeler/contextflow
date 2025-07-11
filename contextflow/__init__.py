"""
ContextFlow - AI Session Context & Workflow Automation

Never lose context between AI sessions again.

This package provides enterprise-grade automation for maintaining context
and documentation across AI-assisted work sessions.
"""

__version__ = "1.0.0"
__author__ = "Matt Wheeler"
__email__ = "matt.wheeler70@gmail.com"
__license__ = "MIT"

from .core.session_updater import SessionUpdater
from .core.context_extractor import ContextExtractor
from .core.workflow_manager import WorkflowManager
from .core.config import ContextFlowConfig

__all__ = [
    "SessionUpdater",
    "ContextExtractor",
    "WorkflowManager",
    "ContextFlowConfig",
]
