"""
Script to run the Streamlit app for the CLO Generator.
"""

import streamlit as st
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the app module
from app import main

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Run the Streamlit app
    main()
