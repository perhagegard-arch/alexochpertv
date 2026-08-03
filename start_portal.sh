#!/bin/bash
set -e
cd "$(dirname "$0")"
exec .venv/bin/gunicorn \
  --bind 0.0.0.0:8080 \
  --workers 1 \
  --threads 4 \
  --timeout 30 \
  "backend.main:app"
