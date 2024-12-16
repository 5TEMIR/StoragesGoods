from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, receipt_repo, get_current_user, check_for_admin_access
from project.schemas.receipt import *
from project.core.exceptions import *

receipt_router = APIRouter()


@receipt_router.get(
    "/all_receipts",
    response_model=list[ReceiptSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_receipts() -> list[ReceiptSchema]:
    async with database.session() as session:
        all_receipts = await receipt_repo.get_all_receipts(session=session)
    return all_receipts


@receipt_router.get(
    "/receipt/{receipt_id}",
    response_model=ReceiptSchema,
    status_code=status.HTTP_200_OK
)
async def get_receipt_by_id(receipt_id: int) -> ReceiptSchema:
    try:
        async with database.session() as session:
            receipt = await receipt_repo.get_receipt_by_id(session=session, receipt_id=receipt_id)
    except ReceiptNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return receipt


@receipt_router.post("/add_receipt", response_model=ReceiptSchema, status_code=status.HTTP_201_CREATED)
async def add_receipt(receipt_dto: ReceiptCreateUpdateSchema,
                      current_user: UserSchema = Depends(get_current_user), ) -> ReceiptSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_receipt = await receipt_repo.create_receipt(session=session, receipt=receipt_dto)
    except ReceiptAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_receipt


@receipt_router.put(
    "/update_receipt/{receipt_id}",
    response_model=ReceiptSchema,
    status_code=status.HTTP_200_OK,
)
async def update_receipt(receipt_id: int, receipt_dto: ReceiptCreateUpdateSchema,
                         current_user: UserSchema = Depends(get_current_user), ) -> ReceiptSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_receipt = await receipt_repo.update_receipt(
                session=session,
                receipt_id=receipt_id,
                receipt=receipt_dto,
            )
    except ReceiptNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_receipt


@receipt_router.delete("/delete_receipt/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_receipt(receipt_id: int, current_user: UserSchema = Depends(get_current_user), ) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            receipt = await receipt_repo.delete_receipt(session=session, receipt_id=receipt_id)
    except ReceiptNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return receipt
