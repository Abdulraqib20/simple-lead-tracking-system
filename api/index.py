"""
Vercel entry point for the Lead Tracking System API.
This file exports the FastAPI app for Vercel's serverless functions.
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the FastAPI app
from main import app

# Export for Vercel
handler = app
