"""
Root conftest.py file to set up the Python path for tests.

This file adds the necessary paths to sys.path to allow both 
relative imports in the app package and importing from app in tests.
"""

import os
import sys

# Get the absolute path to the project root
backend_dir = os.path.dirname(os.path.abspath(__file__))

# Add the backend directory to sys.path if it's not already there
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Add the app directory to sys.path for relative imports within app
app_dir = os.path.join(backend_dir, "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)