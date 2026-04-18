# Work to Be Done

This document tracks small deliverables for the project.

## Future Work

- [ ] Decide how to handle missing-file behavior
  - Since assets reference files on disk, I will eventually need to decide what happens when a file is moved externally, deleted, replaced, or becomes unreadable
  - This is a core lifecycle concern for this kind of app
- [ ] Define python models for database
- [ ] Build datalayer (repository) using SQLAlchemy ORM
- [ ] Define feature sets and related work
  - Base these on small goals such as "as a user, i want to be able to import images"
  - add sub tasks needed to achieve each user story

## Completed

### 0.1.0

- [ ] Define SQLite Schema based on data model (4-18-26)
  - feature/db-schema
- [x] Define mission statement and 10,000ft plan (4-16-26)
  - Captured in the project README as the current product direction and abstract application model.
- [x] Define data model (4-16-26)
  - Based on the mission statement, establish an initial domain model with a clear distinction between image assets and their organizational groupings.
