"""
Fraud Shield — Launcher Script
Run this file from anywhere to start the server.
"""

import os
import sys
import subprocess

# Get paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
MAIN_FILE = os.path.join(BACKEND_DIR, "main.py")

# Check if venv exists and use its python
VENV_PYTHON = os.path.join(BACKEND_DIR, "venv", "Scripts", "python.exe")
if os.path.exists(VENV_PYTHON):
    python_exe = VENV_PYTHON
else:
    python_exe = sys.executable

print("=" * 50)
print("  🛡️  FRAUD SHIELD — Starting Server...")
print("=" * 50)
print(f"  Python : {python_exe}")
print(f"  Backend: {BACKEND_DIR}")
print(f"  URL    : http://localhost:8000")
print("=" * 50)
print()

# Run the backend server
subprocess.run([python_exe, MAIN_FILE], cwd=BACKEND_DIR)
