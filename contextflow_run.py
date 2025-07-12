#!/usr/bin/env python3
"""
ContextFlow Easy Runner
Simple script to run ContextFlow without PATH issues
"""

import sys
import os

# Add the contextflow directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contextflow.cli import main

if __name__ == "__main__":
    main()
