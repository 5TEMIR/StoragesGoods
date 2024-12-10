from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.storageplace import StoragePlaceSchema, StoragePlaceCreateUpdateSchema
from project.infrastructure.postgres.models import StoragePlace

from project.core.exceptions import StoragePlaceNotFound, StoragePlaceAlreadyExists


class StoragePlaceRepository:
    _collection: Type[StoragePlace] = StoragePlace

    async def get_all_storage_places(self, session: AsyncSession) -> list[StoragePlaceSchema]:
        query = select(self._collection)
        storage_places = await session.scalars(query)
        return [StoragePlaceSchema.model_validate(obj=place) for place in storage_places.all()]

    async def get_storage_place_by_id(self, session: AsyncSession, place_id: int) -> StoragePlaceSchema:
        query = select(self._collection).where(self._collection.id == place_id)
        place = await session.scalar(query)
        if not place:
            raise StoragePlaceNotFound(_id=place_id)
        return StoragePlaceSchema.model_validate(obj=place)

    async def create_storage_place(self, session: AsyncSession,
                                   storage_place: StoragePlaceCreateUpdateSchema) -> StoragePlaceSchema:
        query = insert(self._collection).values(storage_place.model_dump()).returning(self._collection)
        try:
            created_place = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise StoragePlaceAlreadyExists(good_id=storage_place.good_id, storage_id=storage_place.storage_id)
        return StoragePlaceSchema.model_validate(obj=created_place)

    async def update_storage_place(self, session: AsyncSession, place_id: int,
                                   storage_place: StoragePlaceCreateUpdateSchema) -> StoragePlaceSchema:
        query = update(self._collection).where(self._collection.id == place_id).values(
            storage_place.model_dump()).returning(self._collection)
        updated_place = await session.scalar(query)
        if not updated_place:
            raise StoragePlaceNotFound(_id=place_id)
        return StoragePlaceSchema.model_validate(obj=updated_place)

    async def delete_storage_place(self, session: AsyncSession, place_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == place_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise StoragePlaceNotFound(_id=place_id)
