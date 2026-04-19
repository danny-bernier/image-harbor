# Work to Be Done

This document tracks small deliverables for the project.

## Future Work

This section is a working backlog of known work.
Stories are intentionally small enough that multiple can be grouped into a single PR when it makes sense.

### Database And Repository Work

- Build repository operations for image assets
- Build repository operations for film rolls
- Build repository operations for user collections
- Build repository operations for tags
- Add repository queries for common library views
  - Recent imports, unviewed assets, needs-editing assets, top-rated assets, and assets by roll or collection.

### Import Pipeline MVP

- Define the import workflow from source files into app-managed storage
  - Decide the steps from selecting files through copied storage and database rows.
- Create import-group records during import
- Copy imported files into the managed storage directory
  - Imported files should land in the app-owned storage layout, not remain coupled to original paths.
- Extract basic file metadata during import
  - Capture size, MIME type, dimensions, and original source information where available.
- Detect duplicate imports
  - Decide how hash/path/name-based duplicate detection should behave.
- Report import failures cleanly
  - Invalid files, unreadable files, or partial imports should be visible and diagnosable.

### Asset Review And Metadata Editing

- Mark assets as viewed during review
- Update asset rating and needs-editing state
- Edit core asset metadata
  - Support updating asset name, description, camera, lens, and capture date fields.
- Attach imported assets to a film roll after import
- Attach or remove tags from assets
- Link edited derivatives back to originals

### Missing File And File Health Behavior

- Define missing-file detection behavior
  - The app should know what happens when a referenced file is moved, deleted, or unreadable.
- Add a file verification scan
  - Periodically or manually confirm that referenced files still exist and are readable.
- Surface missing or broken files in the app state
  - Users should be able to identify assets needing repair.
- Define repair behavior for broken file references
  - Decide whether the app supports relinking, reimporting, or marking assets as unavailable.

### Library Browsing MVP

- Build a basic library query model for browsing assets
  - Listing, sorting, and pagination/windowing should be defined before UI work grows.
- Add filtering by roll, collection, tag, rating, and needs-editing state
- Add a selected-asset detail view model
- Define a review queue query
  - Support browsing assets that are new, un-viewed, or marked for editing.

### Desktop UI Skeleton

- Create the first PySide6 application shell
- Add a library grid placeholder screen
- Add a right-side inspector/details panel
- Add placeholder screens for rolls, collections, and import flow

### Image Processing And Previews

- Generate thumbnails for imported assets
  - Persist thumbnail paths and define thumbnail generation timing.
- Generate larger preview images for detail view
  - Keep preview generation separate from originals.
- Add basic rotate support for harbor-managed files
- Define preview/thumbnail invalidation behavior
  - Changes to images should not leave stale derived files behind.

### Export Workflows

- Export assets marked as needs-editing to a chosen folder
- Export collections or rolls as zip archives
- Export individual assets to alternate formats
  - Use Magick cli potentially?
  - Define which export transforms are supported initially.
- Keep export actions separate from tracked app state
  - Exported files should not be managed library files.

### Backup And Restore

- Define what must be backed up
  - Database, managed image files, previews, thumbnails, or some subset.
- Add a manual backup workflow
  - Start with explicit user-triggered backup instead of continuous sync.
- Add a restore workflow for a backup set
- Decide whether local backup and cloud backup are separate features
  - Do not couple those concerns too early.

### Testing And Developer Confidence

- Add pytest and a basic test layout
  - Establish test locations, fixtures, and naming conventions.
- Add migration smoke tests
  - Verify a database can upgrade from empty to head reliably.
- Add repository tests against disposable SQLite databases
- Add import workflow tests
  - File copying, metadata extraction, and duplicate handling need coverage.
- Add a simple CI workflow for tests

## Completed

### 0.1.0
- **feature/startup-polish** (4-18-26)
  - Define a small application service/repository layer boundary
  - Add structured startup error handling and user-facing failure logging
  - Skip Alembic work when the database is already at the requested revision
- **feature/db-schema** (4-18-26)
  - Add a simple CI workflow for lint
  - Enforce code formatting with hooks
  - Define SQLite Schema based on data
  - Improved environment setup, added ez dev script
  - Added properties, logging, and other general config
  - Wire the real application entrypoint through startup initialization
  - Add a migration workflow note for future schema changes
  - Define SQLAlchemy models for database
- **feature/initial** (4-16-26)
  - Define mission statement and 10,000ft plan
    - Captured in the project README as the current product direction and abstract application model.
  - Define data model abstractly
    - Based on the mission statement, establish an initial domain model with a clear distinction between image assets and their organizational groupings.
