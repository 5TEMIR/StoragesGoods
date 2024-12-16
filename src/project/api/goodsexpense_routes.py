from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, goods_expense_repo, get_current_user, check_for_admin_access
from project.schemas.goodsexpense import GoodsExpenseSchema
from project.core.exceptions import GoodsExpenseNotFound, GoodsExpenseAlreadyExists

goods_expense_router = APIRouter()


@goods_expense_router.get(
    "/goods_expense/{expense_id}",
    response_model=list[GoodsExpenseSchema],
    status_code=status.HTTP_200_OK
)
async def get_goods_expenses_by_expense_id(expense_id: int) -> list[GoodsExpenseSchema]:
    try:
        async with database.session() as session:
            all_expenses = await goods_expense_repo.get_goods_expenses_by_expense_id(session=session,
                                                                                     expense_id=expense_id)
    except GoodsExpenseNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return all_expenses


@goods_expense_router.post("/add_goods_expense", response_model=GoodsExpenseSchema, status_code=status.HTTP_201_CREATED)
async def add_goods_expense(expense_dto: GoodsExpenseSchema,
                            current_user: UserSchema = Depends(get_current_user), ) -> GoodsExpenseSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_expense = await goods_expense_repo.create_goods_expense(session=session, expense=expense_dto)
    except GoodsExpenseAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_expense


@goods_expense_router.delete("/delete_goods_expense/{expense_id}/{storage_place_id}",
                             status_code=status.HTTP_204_NO_CONTENT)
async def delete_goods_expense(expense_id: int, storage_place_id: int,
                               current_user: UserSchema = Depends(get_current_user), ) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            goodsexpense = await goods_expense_repo.delete_goods_expense(session=session, expense_id=expense_id,
                                                                         storage_place_id=storage_place_id)
    except GoodsExpenseNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return goodsexpense
