#!/usr/bin/env python3
"""
Stock Sentiment Analyzer GUI
Run this script to start the graphical user interface.
"""

import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.gui.app import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)