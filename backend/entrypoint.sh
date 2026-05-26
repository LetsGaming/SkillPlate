#!/bin/sh
set -e

echo "--- Environment Variables Check ---"
echo "PORT is set to: $PORT"
echo "WORKERS is set to: $WORKERS"
echo "-----------------------------------"

exec gunicorn run:app \
  --bind 0.0.0.0:"${PORT}" \
  --workers "${WORKERS}" \
  --access-logfile - \
  --error-logfile -