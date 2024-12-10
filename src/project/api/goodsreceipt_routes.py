from fastapi import APIRouter, HTTPException, status

from project.api.depends import database, goods_receipt_repo
from project.schemas.goodsreceipt import *
from project.core.exceptions import *

goods_receipt_router = APIRouter()


@goods_receipt_router.get(
    "/goods_receipt/{receipt_id}",
    response_model=list[GoodsReceiptSchema],
    status_code=status.HTTP_200_OK
)
async def get_goods_receipts_by_receipt_id(receipt_id: int) -> list[GoodsReceiptSchema]:
    try:
        async with database.session() as session:
            all_receipts = await goods_receipt_repo.get_goods_receipts_by_receipt_id(session=session,
                                                                                     receipt_id=receipt_id)
    except GoodsReceiptNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return all_receipts


@goods_receipt_router.post("/add_goods_receipt", response_model=GoodsReceiptSchema, status_code=status.HTTP_201_CREATED)
async def add_goods_receipt(receipt_dto: GoodsReceiptSchema) -> GoodsReceiptSchema:
    try:
        async with database.session() as session:
            new_receipt = await goods_receipt_repo.create_goods_receipt(session=session, receipt=receipt_dto)
    except GoodsReceiptAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_receipt


@goods_receipt_router.delete("/delete_goods_receipt/{receipt_id}/{storage_place_id}",
                             status_code=status.HTTP_204_NO_CONTENT)
async def delete_goods_receipt(receipt_id: int, storage_place_id: int) -> None:
    try:
        async with database.session() as session:
            goodsreceipt = await goods_receipt_repo.delete_goods_receipt(session=session, receipt_id=receipt_id,
                                                                         storage_place_id=storage_place_id)
    except GoodsReceiptNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return goodsreceipt
