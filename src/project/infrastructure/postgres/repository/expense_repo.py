from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.expense import ExpenseSchema, ExpenseCreateUpdateSchema
from project.infrastructure.postgres.models import Expense

from project.core.exceptions import ExpenseNotFound, ExpenseAlreadyExists, ErrorFound


class ExpenseRepository:
    _collection: Type[Expense] = Expense

    async def get_all_expenses(self, session: AsyncSession) -> list[ExpenseSchema]:
        query = select(self._collection)
        expenses = await session.scalars(query)
        return [ExpenseSchema.model_validate(obj=expense) for expense in expenses.all()]

    async def get_expense_by_id(self, session: AsyncSession, expense_id: int) -> ExpenseSchema:
        query = select(self._collection).where(self._collection.id == expense_id)
        expense = await session.scalar(query)
        if not expense:
            raise ExpenseNotFound(_id=expense_id)
        return ExpenseSchema.model_validate(obj=expense)

    async def create_expense(self, session: AsyncSession, expense: ExpenseCreateUpdateSchema) -> ExpenseSchema:
        query = insert(self._collection).values(expense.model_dump()).returning(self._collection)
        try:
            created_expense = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise ErrorFound(err=repr(error))
        return ExpenseSchema.model_validate(obj=created_expense)

    async def update_expense(self, session: AsyncSession, expense_id: int,
                             expense: ExpenseCreateUpdateSchema) -> ExpenseSchema:
        query = update(self._collection).where(self._collection.id == expense_id).values(
            expense.model_dump()).returning(self._collection)
        try:
            updated_expense = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise ErrorFound(err=repr(error))
        if not updated_expense:
            raise ExpenseNotFound(_id=expense_id)
        return ExpenseSchema.model_validate(obj=updated_expense)

    async def delete_expense(self, session: AsyncSession, expense_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == expense_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ExpenseNotFound(_id=expense_id)
