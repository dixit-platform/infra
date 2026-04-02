#!/bin/bash
# One-click AWS project setup/teardown script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure Python environment has required packages
echo "Checking dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

# Run the management script
python3 manage_project.py "$@"
