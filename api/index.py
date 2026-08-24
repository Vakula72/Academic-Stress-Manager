"""Vercel serverless entrypoint for the Flask application."""

import os
import sys
import tempfile

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Vercel functions can only write reliably to /tmp. This keeps SQLite from
# crashing during cold starts when DATABASE_URL/DATABASE_PATH is not configured.
os.environ.setdefault("DATABASE_PATH", os.path.join(tempfile.gettempdir(), "academic_stress_manager.db"))

from app import app  # noqa: E402

