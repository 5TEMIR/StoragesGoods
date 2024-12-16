from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, goods_transfer_repo, get_current_user, check_for_admin_access
from project.schemas.goodstransfer import *
from project.core.exceptions import *

goods_transfer_router = APIRouter()


@goods_transfer_router.get(
    "/all_goods_transfers",
    response_model=list[GoodsTransferSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_goods_transfers() -> list[GoodsTransferSchema]:
    async with database.session() as session:
        all_transfers = await goods_transfer_repo.get_all_goods_transfers(session=session)
    return all_transfers


@goods_transfer_router.get(
    "/goods_transfer/{transfer_id}",
    response_model=GoodsTransferSchema,
    status_code=status.HTTP_200_OK
)
async def get_goods_transfer_by_id(transfer_id: int) -> GoodsTransferSchema:
    try:
        async with database.session() as session:
            transfer = await goods_transfer_repo.get_goods_transfer_by_id(session=session, transfer_id=transfer_id)
    except GoodsTransferNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return transfer


@goods_transfer_router.post("/add_goods_transfer", response_model=GoodsTransferSchema,
                            status_code=status.HTTP_201_CREATED)
async def add_goods_transfer(transfer_dto: GoodsTransferCreateUpdateSchema,
                             current_user: UserSchema = Depends(get_current_user), ) -> GoodsTransferSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_transfer = await goods_transfer_repo.create_goods_transfer(session=session, transfer=transfer_dto)
    except GoodsTransferAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_transfer


@goods_transfer_router.put(
    "/update_goods_transfer/{transfer_id}",
    response_model=GoodsTransferSchema,
    status_code=status.HTTP_200_OK,
)
async def update_goods_transfer(transfer_id: int, transfer_dto: GoodsTransferCreateUpdateSchema,
                                current_user: UserSchema = Depends(get_current_user), ) -> GoodsTransferSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_transfer = await goods_transfer_repo.update_goods_transfer(
                session=session,
                transfer_id=transfer_id,
                transfer=transfer_dto,
            )
    except GoodsTransferNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_transfer


@goods_transfer_router.delete("/delete_goods_transfer/{transfer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goods_transfer(transfer_id: int, current_user: UserSchema = Depends(get_current_user), ) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            goodstransfer = await goods_transfer_repo.delete_goods_transfer(session=session, transfer_id=transfer_id)
    except GoodsTransferNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return goodstransfer
