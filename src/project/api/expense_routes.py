from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, expense_repo, get_current_user, check_for_admin_access
from project.schemas.expense import *
from project.core.exceptions import *

expense_router = APIRouter()


@expense_router.get(
    "/all_expenses",
    response_model=list[ExpenseSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_expenses() -> list[ExpenseSchema]:
    async with database.session() as session:
        all_expenses = await expense_repo.get_all_expenses(session=session)
    return all_expenses


@expense_router.get(
    "/expense/{expense_id}",
    response_model=ExpenseSchema,
    status_code=status.HTTP_200_OK
)
async def get_expense_by_id(expense_id: int) -> ExpenseSchema:
    try:
        async with database.session() as session:
            expense = await expense_repo.get_expense_by_id(session=session, expense_id=expense_id)
    except ExpenseNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return expense


@expense_router.post("/add_expense", response_model=ExpenseSchema, status_code=status.HTTP_201_CREATED)
async def add_expense(expense_dto: ExpenseCreateUpdateSchema,
                      current_user: UserSchema = Depends(get_current_user), ) -> ExpenseSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_expense = await expense_repo.create_expense(session=session, expense=expense_dto)
    except ExpenseAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_expense


@expense_router.put(
    "/update_expense/{expense_id}",
    response_model=ExpenseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_expense(expense_id: int, expense_dto: ExpenseCreateUpdateSchema,
                         current_user: UserSchema = Depends(get_current_user), ) -> ExpenseSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_expense = await expense_repo.update_expense(
                session=session,
                expense_id=expense_id,
                expense=expense_dto,
            )
    except ExpenseNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_expense


@expense_router.delete("/delete_expense/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, current_user: UserSchema = Depends(get_current_user),) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            expense = await expense_repo.delete_expense(session=session, expense_id=expense_id)
    except ExpenseNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return expense
