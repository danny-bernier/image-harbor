"""Application-specific error types."""

from collections.abc import Mapping
from typing import Any


class StartupError(RuntimeError):
    """Represent an application startup failure with structured context.

    Args:
        message: The human-readable startup failure message.
        context: Optional key/value details that add failure context.
    """

    def __init__(self, message: str, *, context: Mapping[str, Any] | None = None) -> None:
        """Initialize the startup error.

        Args:
            message: The human-readable startup failure message.
            context: Optional key/value details that add failure context.
        """

        super().__init__(message)
        self.context = dict(context or {})

    def __str__(self) -> str:
        """Render the error message with any available context.

        Returns:
            str: The formatted startup error message.
        """

        message = super().__str__()
        if not self.context:
            return message

        context_text = ", ".join(f"{key}={value!r}" for key, value in sorted(self.context.items()))
        return f"{message} ({context_text})"
