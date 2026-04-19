#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

export PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export APP_DATA_PATH="${APP_DATA_PATH:-$REPO_ROOT/out/app/data}"
export APP_CONFIG_PATH="${APP_CONFIG_PATH:-$REPO_ROOT/out/app/config}"
export APP_CACHE_PATH="${APP_CACHE_PATH:-$REPO_ROOT/out/app/cache}"

mkdir -p "$APP_DATA_PATH" "$APP_CONFIG_PATH" "$APP_CACHE_PATH"

if [[ -x "$REPO_ROOT/.venv/Scripts/python.exe" ]]; then
	PYTHON_BIN="$REPO_ROOT/.venv/Scripts/python.exe"
elif [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
	PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
else
	PYTHON_BIN="python"
fi

echo "Using Python: $PYTHON_BIN"
echo "Using PYTHONPATH: $PYTHONPATH"
echo "Using APP_DATA_PATH: $APP_DATA_PATH"
echo "Using APP_CONFIG_PATH: $APP_CONFIG_PATH"
echo "Using APP_CACHE_PATH: $APP_CACHE_PATH"

exec "$PYTHON_BIN" "$REPO_ROOT/src/main.py"
