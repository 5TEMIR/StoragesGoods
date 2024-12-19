from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, good_repo, get_current_user, check_for_admin_access
from project.schemas.good import *
from project.core.exceptions import *

good_router = APIRouter()


@good_router.get(
    "/all_goods",
    response_model=list[GoodSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_goods() -> list[GoodSchema]:
    async with database.session() as session:
        all_goods = await good_repo.get_all_goods(session=session)
    return all_goods


@good_router.get(
    "/good/{good_id}",
    response_model=GoodSchema,
    status_code=status.HTTP_200_OK
)
async def get_good_by_id(good_id: int) -> GoodSchema:
    try:
        async with database.session() as session:
            good = await good_repo.get_good_by_id(session=session, good_id=good_id)
    except GoodNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return good


@good_router.post("/add_good", response_model=GoodSchema, status_code=status.HTTP_201_CREATED)
async def add_good(good_dto: GoodCreateUpdateSchema, current_user: UserSchema = Depends(get_current_user),) -> GoodSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_good = await good_repo.create_good(session=session, good=good_dto)
    except ErrorFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_good


@good_router.put(
    "/update_good/{good_id}",
    response_model=GoodSchema,
    status_code=status.HTTP_200_OK,
)
async def update_good(good_id: int, good_dto: GoodCreateUpdateSchema, current_user: UserSchema = Depends(get_current_user),) -> GoodSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_good = await good_repo.update_good(
                session=session,
                good_id=good_id,
                good=good_dto,
            )
    except GoodNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except ErrorFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return updated_good


@good_router.delete("/delete_good/{good_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_good(good_id: int, current_user: UserSchema = Depends(get_current_user),) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            good = await good_repo.delete_good(session=session, good_id=good_id)
    except GoodNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return good
