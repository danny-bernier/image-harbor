# Tech Stack

This document is a short reference for the major technologies that shape day-to-day development in Image Harbor.

It is intentionally not a catalog of every Python package in the repo.
If a library is just an implementation detail and developers rarely interact with it directly, it does not need its own section here.

## Current Stack

### Python 3.13

Python is the application language for the project.
It is used for application code, persistence code, migrations, and local developer tooling.

What matters for development:

- The project targets Python `3.13.12`.
- The code uses the `src/` layout.
- Development is expected to happen inside the repository `.venv`.

### pyproject.toml + setuptools

`pyproject.toml` is the main project configuration file.
It defines the package metadata, dependencies, and tool configuration.
`setuptools` is the build backend used to install the project locally.

What matters for development:

- Runtime dependencies live in `pyproject.toml`.
- Tool configuration such as Black and Ruff also lives there.
- `requirements.txt` is only a thin entrypoint for local editable install.

### SQLite

SQLite is the current database engine.
This is a local desktop app, so a file-based database is a reasonable default.

What matters for development:

- The default database is a SQLite file stored in the app-data directory.
- For development or testing, the app data, config, and cache directories can be overridden with environment variables.
- The database is expected to evolve through Alembic migrations rather than ad hoc schema scripts.

### SQLAlchemy

SQLAlchemy is the database toolkit used to define the schema and create database connections.
Right now the project uses SQLAlchemy Core metadata rather than full ORM models.

What matters for development:

- The schema source of truth lives in `src/repository/models.py`.
- Connection and database path helpers live in `src/repository/database.py`.
- Alembic uses this metadata when generating and applying migrations.

Important files:

- `src/repository/models.py`
- `src/repository/database.py`

### Alembic

Alembic is the database migration system.
It is the most important infrastructure tool in the current stack, because it controls schema versioning and database upgrades.

What matters for development:

- Each schema change should become a new revision in `alembic/versions/`.
- The current database revision is tracked in the database itself through Alembic's `alembic_version` table.
- The Alembic environment gets the database URL from the repository database helpers.
- Developer databases and future user databases should be upgraded through Alembic, not by manually editing tables.

Typical workflow:

1. Update the schema metadata in `src/repository/models.py`.
2. Create a new Alembic revision.
3. Review and adjust the migration.
4. Upgrade a local dev or test database to head.

Regular commands developers will actually use:

```bash
python -m alembic current
python -m alembic history
python -m alembic upgrade head
python -m alembic downgrade -1
python -m alembic revision --autogenerate -m "describe schema change"
```

If you want to run migrations against a repo-local disposable database instead of the normal app-data database, set the prefixed app path environment variables first.

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

Important files:

- `alembic.ini`
- `alembic/env.py`
- `alembic/versions/`

### VS Code Workspace Tooling

VS Code is the expected local development environment right now.
Formatting and lint behavior are primarily configured through workspace settings and recommended extensions rather than regular CLI usage.

What matters for development:

- `.vscode/settings.json` defines the workspace editor behavior.
- `.vscode/extensions.json` recommends the Python, Black, Ruff, and PlantUML extensions.
- `.editorconfig` keeps whitespace and indentation consistent across editors.

### PlantUML

PlantUML is used for diagrams that should live in source control as text.
At the moment this mainly matters for schema and architecture diagrams.

What matters for development:

- Diagram sources live in the docs/diagram locations.
- Developers edit the `.puml` source, not just exported images.

## Planned Stack

These are still part of the intended direction of the app, but they are not the main day-to-day technologies in the repo yet.

### PySide6

PySide6 is the planned desktop UI framework.
It will likely become the primary UI technology once the application moves beyond current scaffolding and schema work.

### EXIF + image processing libraries

The project will likely add dedicated metadata and image-processing libraries later for import-time metadata extraction, thumbnail generation, previews, and simple edits.

The exact packages are still less important than the role they will play:

- reading image metadata
- generating previews and thumbnails
- performing simple image transforms

### pytest

`pytest` is the likely future test runner once the project adds a real test suite.

## Files Worth Knowing

- `pyproject.toml`: project metadata and tool configuration
- `requirements.txt`: local editable install entrypoint
- `src/repository/models.py`: SQLAlchemy schema metadata
- `src/repository/database.py`: database path and engine helpers
- `alembic.ini`: Alembic configuration
- `alembic/env.py`: Alembic runtime environment
- `alembic/versions/`: schema revision history
- `.vscode/settings.json`: workspace editor behavior
- `.vscode/extensions.json`: recommended VS Code extensions
- `.editorconfig`: cross-editor formatting defaults
