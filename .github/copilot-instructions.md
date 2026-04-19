# Copilot Instructions

## Code Organization

- Prefer keeping logic inline when it is only used in one place.
- Do not extract single-use helper functions unless the extraction clearly improves readability, reuse, or testability.
- Favor direct, easy-to-follow code over small indirection layers.
- When in doubt, optimize for local readability in the file being edited.

## Documentation

- Add docstrings to all public functions, methods, and classes.
- Use the same autodocstring-style format consistently across the project.