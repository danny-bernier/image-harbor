#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

if [[ -x "$REPO_ROOT/.venv/Scripts/python.exe" ]]; then
	PYTHON_BIN="$REPO_ROOT/.venv/Scripts/python.exe"
elif [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
	PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
else
	PYTHON_BIN="python"
fi

echo "Using Python: $PYTHON_BIN"
echo "Running Black check..."
"$PYTHON_BIN" -m black --check src alembic

echo "Running Ruff..."
"$PYTHON_BIN" -m ruff check src alembic
