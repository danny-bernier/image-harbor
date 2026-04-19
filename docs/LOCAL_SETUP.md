# Local Environment Setup

This guide assumes you already have the repository cloned locally and are running commands from the repository root.

This project uses a local `.venv` plus `requirements.txt` and `pyproject.toml`.
Pipenv is not part of the workflow.

## 1. Prerequisites

Install Python `3.13.12` before setting up the project.

Optional local tools:

- Windows with Chocolatey: `choco install sqlite`
- macOS with Homebrew: `brew install sqlite`

No separate Chocolatey or Homebrew Alembic package is required. Alembic and SQLAlchemy are installed through the project Python environment.

## 2. Create The Virtual Environment

Create the local virtual environment:

```bash
python -m venv .venv
```

## 3. Activate The Virtual Environment

Activate the environment before installing anything else:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows Git Bash: `source .venv/Scripts/activate`
- macOS/Linux: `source .venv/bin/activate`

## 4. Install Project Dependencies

With the virtual environment active, install the project and developer dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .[dev]
```

## 5. Install The Git Pre-commit Hook

Install the local Git hook:

```bash
python -m pre_commit install
```

This repo uses `pre-commit` to run local quality checks before each commit.
Right now those checks run Ruff first and then Black.

If either tool changes files, the commit stops so you can review the edits, stage them, and commit again.

Useful manual commands:

```bash
python -m pre_commit run --all-files
python -m pre_commit run
```

Use `pre-commit run --all-files` after first-time setup if you want to normalize the whole repo before starting work.

## 6. Run Quality Checks Manually

If you want to run the same Black and Ruff checks outside of the Git hook, use the quality script:

```bash
bash ./scripts/quality.sh
```

This runs the same ad-hoc quality checks that the GitHub `quality` workflow uses.

## 7. Install Recommended VS Code Extensions

Install the recommended workspace extensions from [/.vscode/extensions.json](.vscode/extensions.json).

In VS Code:

1. Run `Extensions: Show Recommended Extensions` from the Command Palette.
2. Install the workspace recommendations.

Formatting is handled by Black. Import sorting and basic lint checks are handled by Ruff.
GitHub also runs both checks through the quality workflow in pull requests and pushes to `main`.

## 8. Initialize Or Inspect The Local Database

Common Alembic commands:

```bash
python -m alembic upgrade head
python -m alembic current
python -m alembic revision --autogenerate -m "describe schema change"
```

By default, Alembic uses the application SQLite path under the app data directory resolved by `src/app_properties.py`.
For local development, you can point the app and Alembic at repo-local directories by setting the prefixed app path environment variables before running commands.

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

## 9. Run The App Locally

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
