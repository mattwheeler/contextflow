#!/usr/bin/env python3
"""
ContextFlow Setup Script
AI Session Context & Workflow Automation
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="contextflow",
    version="1.0.0",
    author="Matt Wheeler",
    author_email="matt.wheeler70@gmail.com",
    description="AI Session Context & Workflow Automation - Never lose context between AI sessions again",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattwheeler/contextflow",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Groupware",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "contextflow=contextflow.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "contextflow": [
            "templates/*.yaml",
            "templates/*.md",
            "config/*.env",
        ],
    },
    keywords=[
        "ai", "automation", "documentation", "workflow", "context", 
        "jira", "confluence", "github", "productivity", "team"
    ],
    project_urls={
        "Bug Reports": "https://github.com/mattwheeler/contextflow/issues",
        "Source": "https://github.com/mattwheeler/contextflow",
        "Documentation": "https://github.com/mattwheeler/contextflow#readme",
    },
)
