# Copilot Instructions

## Code Organization

- Prefer keeping logic inline when it is only used in one place.
- Do not extract single-use helper functions unless the extraction clearly improves readability, reuse, or testability.
- Favor direct, easy-to-follow code over small indirection layers.
- When in doubt, optimize for local readability in the file being edited.

## Documentation

- Add a module docstring to every Python file.
- Add docstrings to all public functions, methods, and classes.
- Use the same autodocstring-style format consistently across the project. See examples:
    """_summary_

    Args:
        engine (Engine): _description_

    Yields:
        Generator[Connection]: _description_
    """
    """Get a configured logger for the supplied module or component name.

    Args:
        name: The logger name to retrieve.

    Returns:
        Logger: A logger configured with the application's root logging settings.
    """

## Package Structure

- `__init__.py` files should be omitted unless the package requires explicit initialization or exports.
