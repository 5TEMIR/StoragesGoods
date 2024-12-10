from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.receipt import ReceiptSchema, ReceiptCreateUpdateSchema
from project.infrastructure.postgres.models import Receipt

from project.core.exceptions import ReceiptNotFound, ReceiptAlreadyExists


class ReceiptRepository:
    _collection: Type[Receipt] = Receipt

    async def get_all_receipts(self, session: AsyncSession) -> list[ReceiptSchema]:
        query = select(self._collection)
        receipts = await session.scalars(query)
        return [ReceiptSchema.model_validate(obj=receipt) for receipt in receipts.all()]

    async def get_receipt_by_id(self, session: AsyncSession, receipt_id: int) -> ReceiptSchema:
        query = select(self._collection).where(self._collection.id == receipt_id)
        receipt = await session.scalar(query)
        if not receipt:
            raise ReceiptNotFound(_id=receipt_id)
        return ReceiptSchema.model_validate(obj=receipt)

    async def create_receipt(self, session: AsyncSession, receipt: ReceiptCreateUpdateSchema) -> ReceiptSchema:
        query = insert(self._collection).values(receipt.model_dump()).returning(self._collection)
        try:
            created_receipt = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise ReceiptAlreadyExists(receipt_date=receipt.receip_date, supplier_id=receipt.supplier_id)
        return ReceiptSchema.model_validate(obj=created_receipt)

    async def update_receipt(self, session: AsyncSession, receipt_id: int,
                             receipt: ReceiptCreateUpdateSchema) -> ReceiptSchema:
        query = update(self._collection).where(self._collection.id == receipt_id).values(
            receipt.model_dump()).returning(self._collection)
        updated_receipt = await session.scalar(query)
        if not updated_receipt:
            raise ReceiptNotFound(_id=receipt_id)
        return ReceiptSchema.model_validate(obj=updated_receipt)

    async def delete_receipt(self, session: AsyncSession, receipt_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == receipt_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ReceiptNotFound(_id=receipt_id)
