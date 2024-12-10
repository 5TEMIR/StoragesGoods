from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.goodsreceipt import *
from project.infrastructure.postgres.models import GoodsReceipt

from project.core.exceptions import GoodsReceiptNotFound, GoodsReceiptAlreadyExists


class GoodsReceiptRepository:
    _collection: Type[GoodsReceipt] = GoodsReceipt

    async def create_goods_receipt(self, session: AsyncSession,
                                   receipt: GoodsReceiptSchema) -> GoodsReceiptSchema:
        query = insert(self._collection).values(receipt.model_dump()).returning(self._collection)
        try:
            created_receipt = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise GoodsReceiptAlreadyExists(receipt_id=receipt.receipt_id, storage_place_id=receipt.storage_place_id)
        return GoodsReceiptSchema.model_validate(obj=created_receipt)

    async def delete_goods_receipt(self, session: AsyncSession, receipt_id: int, storage_place_id: int) -> None:
        query = delete(self._collection).where(
            self._collection.receipt_id == receipt_id,
            self._collection.storage_place_id == storage_place_id
        )
        result = await session.execute(query)
        if not result.rowcount:
            raise GoodsReceiptNotFound(receipt_id=receipt_id)

    async def get_goods_receipts_by_receipt_id(
            self, session: AsyncSession, receipt_id: int
    ) -> list[GoodsReceiptSchema]:
        query = select(self._collection).where(self._collection.receipt_id == receipt_id)
        goods_receipts = await session.scalars(query)
        if not goods_receipts:
            raise GoodsReceiptNotFound(receipt_id=receipt_id)
        return [GoodsReceiptSchema.model_validate(obj=receipt) for receipt in goods_receipts.all()]
