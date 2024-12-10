from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.storagemethod import StorageMethodSchema, StorageMethodCreateUpdateSchema
from project.infrastructure.postgres.models import StorageMethod

from project.core.exceptions import StorageMethodNotFound, StorageMethodAlreadyExists


class StorageMethodRepository:
    _collection: Type[StorageMethod] = StorageMethod

    async def get_all_storage_methods(self, session: AsyncSession) -> list[StorageMethodSchema]:
        query = select(self._collection)
        storage_methods = await session.scalars(query)
        return [StorageMethodSchema.model_validate(obj=method) for method in storage_methods.all()]

    async def get_storage_method_by_id(self, session: AsyncSession, storage_method_id: int) -> StorageMethodSchema:
        query = select(self._collection).where(self._collection.id == storage_method_id)
        storage_method = await session.scalar(query)
        if not storage_method:
            raise StorageMethodNotFound(_id=storage_method_id)
        return StorageMethodSchema.model_validate(obj=storage_method)

    async def create_storage_method(self, session: AsyncSession,
                                    storage_method: StorageMethodCreateUpdateSchema) -> StorageMethodSchema:
        query = insert(self._collection).values(storage_method.model_dump()).returning(self._collection)
        try:
            created_storage_method = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise StorageMethodAlreadyExists(name=storage_method.name)
        return StorageMethodSchema.model_validate(obj=created_storage_method)

    async def update_storage_method(self, session: AsyncSession, storage_method_id: int,
                                    storage_method: StorageMethodCreateUpdateSchema) -> StorageMethodSchema:
        query = update(self._collection).where(self._collection.id == storage_method_id).values(
            storage_method.model_dump()).returning(self._collection)
        updated_storage_method = await session.scalar(query)
        if not updated_storage_method:
            raise StorageMethodNotFound(_id=storage_method_id)
        return StorageMethodSchema.model_validate(obj=updated_storage_method)

    async def delete_storage_method(self, session: AsyncSession, storage_method_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == storage_method_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise StorageMethodNotFound(_id=storage_method_id)
