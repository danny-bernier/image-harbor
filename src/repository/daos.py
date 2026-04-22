"""SQLAlchemy DAO helpers for Image Harbor persistence operations."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import Engine, Select, select
from sqlalchemy.orm import Session, sessionmaker

from client.database_client import create_database_engine
from model.database.models import (
    File,
    FilmRoll,
    ImageAsset,
    ImportGroup,
    Tag,
    TagToImageAsset,
    UserCollection,
    UserCollectionToImageAsset,
)

ModelT = TypeVar("ModelT")


def create_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    """Create a sessionmaker configured for Image Harbor repositories.

    Args:
        engine: Optional SQLAlchemy engine. If omitted, the app database engine is used.

    Returns:
        sessionmaker[Session]: A configured SQLAlchemy session factory.
    """

    return sessionmaker(bind=engine or create_database_engine(), autoflush=False, expire_on_commit=False, future=True)


class BaseDAO(Generic[ModelT]):
    """Provide common CRUD behavior for SQLAlchemy mapped models."""

    def __init__(self, session: Session, model_type: type[ModelT]) -> None:
        """Initialize a DAO instance.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
            model_type: ORM model class managed by this DAO.
        """

        self._session = session
        self._model_type = model_type

    def add(self, entity: ModelT, *, commit: bool = False) -> ModelT:
        """Add an entity to the session and optionally commit.

        Args:
            entity: Model instance to add.
            commit: Whether to commit immediately.

        Returns:
            ModelT: The persisted entity.
        """

        self._session.add(entity)
        if commit:
            self._session.commit()
            self._session.refresh(entity)
        return entity

    def get(self, identity: Any) -> ModelT | None:
        """Fetch a model row by primary key identity.

        Args:
            identity: Primary key value, or tuple for composite keys.

        Returns:
            ModelT | None: The matching entity if found.
        """

        return self._session.get(self._model_type, identity)

    def list(self, *, limit: int | None = None, offset: int = 0) -> list[ModelT]:
        """List model rows with optional pagination.

        Args:
            limit: Optional max row count.
            offset: Optional row offset.

        Returns:
            list[ModelT]: Matching model rows.
        """

        statement: Select[tuple[ModelT]] = select(self._model_type).offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        return list(self._session.scalars(statement))

    def find_one(self, **filters: Any) -> ModelT | None:
        """Find a single row using equality filters.

        Args:
            **filters: Column-to-value equality filters.

        Returns:
            ModelT | None: A single matching row, if any.
        """

        statement: Select[tuple[ModelT]] = select(self._model_type).filter_by(**filters)
        return self._session.scalar(statement)

    def delete(self, entity: ModelT, *, commit: bool = False) -> None:
        """Delete an entity from the session and optionally commit.

        Args:
            entity: Model instance to delete.
            commit: Whether to commit immediately.
        """

        self._session.delete(entity)
        if commit:
            self._session.commit()

    def delete_by_identity(self, identity: Any, *, commit: bool = False) -> bool:
        """Delete a row by primary key identity.

        Args:
            identity: Primary key value, or tuple for composite keys.
            commit: Whether to commit immediately.

        Returns:
            bool: True if a row was found and deleted; otherwise False.
        """

        entity = self.get(identity)
        if entity is None:
            return False
        self.delete(entity, commit=commit)
        return True


class FileDAO(BaseDAO[File]):
    """DAO for file rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the file DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, File)

    def get_by_path(self, path: str) -> File | None:
        """Fetch a file row by absolute storage path.

        Args:
            path: Absolute file path stored in the files table.

        Returns:
            File | None: The matching file row, if present.
        """

        return self.find_one(path=path)


class FilmRollDAO(BaseDAO[FilmRoll]):
    """DAO for film roll rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the film roll DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, FilmRoll)


class ImportGroupDAO(BaseDAO[ImportGroup]):
    """DAO for import group rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the import group DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, ImportGroup)

    def get_by_storage_dir(self, storage_dir: str) -> ImportGroup | None:
        """Fetch an import group by storage directory.

        Args:
            storage_dir: Managed directory path for a single import group.

        Returns:
            ImportGroup | None: The matching import group row, if present.
        """

        return self.find_one(storage_dir=storage_dir)


class ImageAssetDAO(BaseDAO[ImageAsset]):
    """DAO for image asset rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the image asset DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, ImageAsset)


class UserCollectionDAO(BaseDAO[UserCollection]):
    """DAO for user collection rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the user collection DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, UserCollection)


class UserCollectionToImageAssetDAO(BaseDAO[UserCollectionToImageAsset]):
    """DAO for user collection to image asset link rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the collection link DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, UserCollectionToImageAsset)

    def get_link(self, user_collection_id: int, image_asset_id: int) -> UserCollectionToImageAsset | None:
        """Fetch a collection-asset link by composite key.

        Args:
            user_collection_id: User collection identifier.
            image_asset_id: Image asset identifier.

        Returns:
            UserCollectionToImageAsset | None: The matching link row, if present.
        """

        return self.get((user_collection_id, image_asset_id))


class TagDAO(BaseDAO[Tag]):
    """DAO for tag rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the tag DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, Tag)

    def get_by_name(self, name: str) -> Tag | None:
        """Fetch a tag by name.

        Args:
            name: Case-insensitive tag name.

        Returns:
            Tag | None: The matching tag row, if present.
        """

        return self.find_one(name=name)


class TagToImageAssetDAO(BaseDAO[TagToImageAsset]):
    """DAO for tag to image asset link rows."""

    def __init__(self, session: Session) -> None:
        """Initialize the tag link DAO.

        Args:
            session: Active SQLAlchemy session used for persistence operations.
        """

        super().__init__(session, TagToImageAsset)

    def get_link(self, tag_id: int, image_asset_id: int) -> TagToImageAsset | None:
        """Fetch a tag-asset link by composite key.

        Args:
            tag_id: Tag identifier.
            image_asset_id: Image asset identifier.

        Returns:
            TagToImageAsset | None: The matching link row, if present.
        """

        return self.get((tag_id, image_asset_id))


__all__ = [
    "BaseDAO",
    "FileDAO",
    "FilmRollDAO",
    "ImportGroupDAO",
    "ImageAssetDAO",
    "UserCollectionDAO",
    "UserCollectionToImageAssetDAO",
    "TagDAO",
    "TagToImageAssetDAO",
    "create_session_factory",
]
