# Copilot Instructions

## Code Organization

- Prefer keeping logic inline when it is only used in one place.
- Do not extract single-use helper functions unless the extraction clearly improves readability, reuse, or testability.
- Favor direct, easy-to-follow code over small indirection layers.
- When in doubt, optimize for local readability in the file being edited.

## Documentation

- Add a module docstring to every Python file.
- Add docstrings to all public functions, methods, and classes.
- Use the same autodocstring-style format consistently across the project.

## Package Structure

- Prefer explicit `__init__.py` files in each Python package and subpackage directory.
- `__init__.py` files may be blank except for a module docstring when no exports are needed.
