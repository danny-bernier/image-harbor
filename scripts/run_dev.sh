#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

export PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export IMAGE_HARBOR_APP_DATA_PATH="${IMAGE_HARBOR_APP_DATA_PATH:-$REPO_ROOT/out/app/data}"
export IMAGE_HARBOR_APP_CONFIG_PATH="${IMAGE_HARBOR_APP_CONFIG_PATH:-$REPO_ROOT/out/app/config}"
export IMAGE_HARBOR_APP_CACHE_PATH="${IMAGE_HARBOR_APP_CACHE_PATH:-$REPO_ROOT/out/app/cache}"
export IMAGE_HARBOR_LOG_LEVEL="${IMAGE_HARBOR_LOG_LEVEL:-DEBUG}"

if [[ -x "$REPO_ROOT/.venv/Scripts/python.exe" ]]; then
	PYTHON_BIN="$REPO_ROOT/.venv/Scripts/python.exe"
elif [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
	PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
else
	PYTHON_BIN="python"
fi

echo "Using Python: $PYTHON_BIN"
echo "Using PYTHONPATH: $PYTHONPATH"
echo "Using IMAGE_HARBOR_APP_DATA_PATH: $IMAGE_HARBOR_APP_DATA_PATH"
echo "Using IMAGE_HARBOR_APP_CONFIG_PATH: $IMAGE_HARBOR_APP_CONFIG_PATH"
echo "Using IMAGE_HARBOR_APP_CACHE_PATH: $IMAGE_HARBOR_APP_CACHE_PATH"
echo "Using IMAGE_HARBOR_LOG_LEVEL: $IMAGE_HARBOR_LOG_LEVEL"

exec "$PYTHON_BIN" "$REPO_ROOT/src/main.py"
