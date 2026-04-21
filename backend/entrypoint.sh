#!/bin/sh

# Use set -e to exit immediately if a command exits with a non-zero status.
set -e

# 1. Verification Step: Print the variables to the log
echo "--- Environment Variables Check ---"
echo "PORT is set to: $PORT"
echo "WORKERS is set to: $WORKERS"
echo "-----------------------------------"

# 2. Substitution Check: Use curly braces and quotes for safety
# Use 'exec' to run gunicorn
exec gunicorn app:app --bind 0.0.0.0:"${PORT}" --workers "${WORKERS}"
