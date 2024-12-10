from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.goodsgroup import GoodsGroupSchema, GoodsGroupCreateUpdateSchema
from project.infrastructure.postgres.models import GoodsGroup

from project.core.exceptions import GoodsGroupNotFound, GoodsGroupAlreadyExists


class GoodsGroupRepository:
    _collection: Type[GoodsGroup] = GoodsGroup

    async def get_all_goods_groups(
            self,
            session: AsyncSession,
    ) -> list[GoodsGroupSchema]:
        query = select(self._collection)

        goods_groups = await session.scalars(query)

        return [GoodsGroupSchema.model_validate(obj=group) for group in goods_groups.all()]

    async def get_goods_group_by_id(
            self,
            session: AsyncSession,
            goods_group_id: int,
    ) -> GoodsGroupSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == goods_group_id)
        )
        goods_group = await session.scalar(query)
        if not goods_group:
            raise GoodsGroupNotFound(_id=goods_group_id)
        return GoodsGroupSchema.model_validate(obj=goods_group)

    async def create_goods_group(
            self,
            session: AsyncSession,
            goods_group: GoodsGroupCreateUpdateSchema,
    ) -> GoodsGroupSchema:
        query = (
            insert(self._collection)
            .values(goods_group.model_dump())
            .returning(self._collection)
        )
        try:
            created_goods_group = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise GoodsGroupAlreadyExists(name=goods_group.name)
        return GoodsGroupSchema.model_validate(obj=created_goods_group)

    async def update_goods_group(
            self,
            session: AsyncSession,
            goods_group_id: int,
            goods_group: GoodsGroupCreateUpdateSchema,
    ) -> GoodsGroupSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == goods_group_id)
            .values(goods_group.model_dump())
            .returning(self._collection)
        )
        updated_goods_group = await session.scalar(query)
        if not updated_goods_group:
            raise GoodsGroupNotFound(_id=goods_group_id)
        return GoodsGroupSchema.model_validate(obj=updated_goods_group)

    async def delete_goods_group(
            self,
            session: AsyncSession,
            goods_group_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == goods_group_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise GoodsGroupNotFound(_id=goods_group_id)
