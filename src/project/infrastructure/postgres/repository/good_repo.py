from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.good import GoodSchema, GoodCreateUpdateSchema
from project.infrastructure.postgres.models import Good

from project.core.exceptions import GoodNotFound, GoodAlreadyExists


class GoodRepository:
    _collection: Type[Good] = Good

    async def get_all_goods(self, session: AsyncSession) -> list[GoodSchema]:
        query = select(self._collection)
        goods = await session.scalars(query)
        return [GoodSchema.model_validate(obj=good) for good in goods.all()]

    async def get_good_by_id(self, session: AsyncSession, good_id: int) -> GoodSchema:
        query = select(self._collection).where(self._collection.id == good_id)
        good = await session.scalar(query)
        if not good:
            raise GoodNotFound(_id=good_id)
        return GoodSchema.model_validate(obj=good)

    async def create_good(self, session: AsyncSession, good: GoodCreateUpdateSchema) -> GoodSchema:
        query = insert(self._collection).values(good.model_dump()).returning(self._collection)
        try:
            created_good = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise GoodAlreadyExists(name=good.name)
        return GoodSchema.model_validate(obj=created_good)

    async def update_good(self, session: AsyncSession, good_id: int, good: GoodCreateUpdateSchema) -> GoodSchema:
        query = update(self._collection).where(self._collection.id == good_id).values(good.model_dump()).returning(
            self._collection)
        updated_good = await session.scalar(query)
        if not updated_good:
            raise GoodNotFound(_id=good_id)
        return GoodSchema.model_validate(obj=updated_good)

    async def delete_good(self, session: AsyncSession, good_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == good_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise GoodNotFound(_id=good_id)
