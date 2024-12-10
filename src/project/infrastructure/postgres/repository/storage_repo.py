from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.storage import StorageSchema, StorageCreateUpdateSchema
from project.infrastructure.postgres.models import Storage

from project.core.exceptions import *


class StorageRepository:
    _collection: Type[Storage] = Storage

    async def get_all_storages(
            self,
            session: AsyncSession,
    ) -> list[StorageSchema]:
        query = select(self._collection)

        storages = await session.scalars(query)

        return [StorageSchema.model_validate(obj=storage) for storage in storages.all()]

    async def get_storage_by_id(
            self,
            session: AsyncSession,
            storage_id: int,
    ) -> StorageSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == storage_id)
        )
        storage = await session.scalar(query)
        if not storage:
            raise StorageNotFound(_id=storage_id)
        return StorageSchema.model_validate(obj=storage)

    async def create_storage(
            self,
            session: AsyncSession,
            storage: StorageCreateUpdateSchema,
    ) -> StorageSchema:
        query = (
            insert(self._collection)
            .values(storage.model_dump())
            .returning(self._collection)
        )
        try:
            created_storage = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise StorageAlreadyExists(address=storage.address)
        return StorageSchema.model_validate(obj=created_storage)

    async def update_storage(
            self,
            session: AsyncSession,
            storage_id: int,
            storage: StorageCreateUpdateSchema,
    ) -> StorageSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == storage_id)
            .values(storage.model_dump())
            .returning(self._collection)
        )
        updated_storage = await session.scalar(query)
        if not updated_storage:
            raise StorageNotFound(_id=storage_id)
        return StorageSchema.model_validate(obj=updated_storage)

    async def delete_storage(
            self,
            session: AsyncSession,
            storage_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == storage_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise StorageNotFound(_id=storage_id)
