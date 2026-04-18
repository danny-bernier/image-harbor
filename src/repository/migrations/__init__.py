"""Migration contracts and migration package exports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from sqlite3 import Connection


class Migration(ABC):
    """Abstract base class that every schema migration must implement."""

    version: int
    description: str

    @abstractmethod
    def upgrade(self, connection: Connection) -> None:
        """Apply the migration to move the schema forward."""

    @abstractmethod
    def downgrade(self, connection: Connection) -> None:
        """Revert the migration to move the schema backward."""


__all__ = ["Migration"]