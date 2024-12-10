from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.goodstransfer import GoodsTransferSchema, GoodsTransferCreateUpdateSchema
from project.infrastructure.postgres.models import GoodsTransfer

from project.core.exceptions import GoodsTransferNotFound, GoodsTransferAlreadyExists


class GoodsTransferRepository:
    _collection: Type[GoodsTransfer] = GoodsTransfer

    async def get_all_goods_transfers(self, session: AsyncSession) -> list[GoodsTransferSchema]:
        query = select(self._collection)
        goods_transfers = await session.scalars(query)
        return [GoodsTransferSchema.model_validate(obj=transfer) for transfer in goods_transfers.all()]

    async def get_goods_transfer_by_id(self, session: AsyncSession, transfer_id: int) -> GoodsTransferSchema:
        query = select(self._collection).where(self._collection.id == transfer_id)
        transfer = await session.scalar(query)
        if not transfer:
            raise GoodsTransferNotFound(_id=transfer_id)
        return GoodsTransferSchema.model_validate(obj=transfer)

    async def create_goods_transfer(self, session: AsyncSession,
                                    transfer: GoodsTransferCreateUpdateSchema) -> GoodsTransferSchema:
        query = insert(self._collection).values(transfer.model_dump()).returning(self._collection)
        try:
            created_transfer = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise GoodsTransferAlreadyExists(quantity=transfer.quantity, transfer_date=transfer.transfer_date,
                                             good_id=transfer.good_id)
        return GoodsTransferSchema.model_validate(obj=created_transfer)

    async def update_goods_transfer(self, session: AsyncSession, transfer_id: int,
                                    transfer: GoodsTransferCreateUpdateSchema) -> GoodsTransferSchema:
        query = update(self._collection).where(self._collection.id == transfer_id).values(
            transfer.model_dump()).returning(self._collection)
        updated_transfer = await session.scalar(query)
        if not updated_transfer:
            raise GoodsTransferNotFound(_id=transfer_id)
        return GoodsTransferSchema.model_validate(obj=updated_transfer)

    async def delete_goods_transfer(self, session: AsyncSession, transfer_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == transfer_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise GoodsTransferNotFound(_id=transfer_id)
