from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.goodsexpense import GoodsExpenseSchema
from project.infrastructure.postgres.models import GoodsExpense

from project.core.exceptions import GoodsExpenseNotFound, GoodsExpenseAlreadyExists, ErrorFound


class GoodsExpenseRepository:
    _collection: Type[GoodsExpense] = GoodsExpense

    async def create_goods_expense(self, session: AsyncSession,
                                    expense: GoodsExpenseSchema) -> GoodsExpenseSchema:
        query = insert(self._collection).values(expense.model_dump()).returning(self._collection)
        try:
            created_expense = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise ErrorFound(err=repr(error))
        return GoodsExpenseSchema.model_validate(obj=created_expense)

    async def delete_goods_expense(self, session: AsyncSession, expense_id: int, storage_place_id: int) -> None:
        query = delete(self._collection).where(
            self._collection.expense_id == expense_id,
            self._collection.storage_place_id == storage_place_id
        )
        result = await session.execute(query)
        if not result.rowcount:
            raise GoodsExpenseNotFound(expense_id=expense_id)

    async def get_goods_expenses_by_expense_id(
            self, session: AsyncSession, expense_id: int
    ) -> list[GoodsExpenseSchema]:
        query = select(self._collection).where(self._collection.expense_id == expense_id)
        goods_expenses = await session.scalars(query)
        if not goods_expenses:
            raise GoodsExpenseNotFound(expense_id=expense_id)
        return [GoodsExpenseSchema.model_validate(obj=expense) for expense in goods_expenses.all()]
