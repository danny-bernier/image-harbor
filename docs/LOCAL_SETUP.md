# Local Environment Setup

This project uses a local `.venv` plus `requirements.txt` and `pyproject.toml`.
Pipenv is not part of the workflow.

Alembic is used for schema versioning and SQLAlchemy is used for schema metadata and database access.

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .[dev]
```

Activate the environment before running the install commands:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows Git Bash: `source .venv/Scripts/activate`
- macOS/Linux: `source .venv/bin/activate`

No separate Chocolatey or Homebrew Alembic package is required. Alembic and SQLAlchemy are installed via `pip` into the project's `.venv`.

Optional local tools:

- Windows with Chocolatey: `choco install sqlite`
- macOS with Homebrew: `brew install sqlite`

Common Alembic commands:

```bash
python -m alembic upgrade head
python -m alembic current
python -m alembic revision --autogenerate -m "describe schema change"
```

By default, Alembic uses the application SQLite path under the app data directory resolved by `src/app_properties.py`. For local development, you can point the app and Alembic at repo-local directories by setting the prefixed app path environment variables before running commands.

Windows PowerShell:

```powershell
$env:IMAGE_HARBOR_APP_DATA_PATH = "$PWD/out/app/data"
$env:IMAGE_HARBOR_APP_CONFIG_PATH = "$PWD/out/app/config"
$env:IMAGE_HARBOR_APP_CACHE_PATH = "$PWD/out/app/cache"
python -m alembic upgrade head
```

macOS/Linux shell:

```bash
export IMAGE_HARBOR_APP_DATA_PATH="$PWD/out/app/data"
export IMAGE_HARBOR_APP_CONFIG_PATH="$PWD/out/app/config"
export IMAGE_HARBOR_APP_CACHE_PATH="$PWD/out/app/cache"
python -m alembic upgrade head
```

## Running The App Locally

The simplest way to run the app in VS Code is through the dev runner script:

```bash
./scripts/run_dev.sh
```

That script:

- sets `PYTHONPATH` to the repo `src` directory
- sets repo-local app data, config, and cache directories by default
- prefers the project's `.venv` interpreter if present
- launches `src/main.py`

The default dev directories used by the script are:

```text
out/app/data
out/app/config
out/app/cache
```

Because the database path is derived from `IMAGE_HARBOR_APP_DATA_PATH`, the default dev database created by the script will be:

```text
out/app/data/image_harbor.db
```

You can still override `IMAGE_HARBOR_APP_DATA_PATH`, `IMAGE_HARBOR_APP_CONFIG_PATH`, and `IMAGE_HARBOR_APP_CACHE_PATH` before running the script if you want to target different locations.

Then install the recommended VS Code extensions from [/.vscode/extensions.json](.vscode/extensions.json).

In VS Code:

1. Run `Extensions: Show Recommended Extensions` from the Command Palette.
2. Install the workspace recommendations.

Formatting is handled by Black. Import sorting and basic lint checks are handled by Ruff.
