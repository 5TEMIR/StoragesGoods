from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, storage_repo, get_current_user, check_for_admin_access
from project.schemas.storage import *
from project.core.exceptions import *

storage_router = APIRouter()


@storage_router.get(
    "/all_storages",
    response_model=list[StorageSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_storages() -> list[StorageSchema]:
    async with database.session() as session:
        all_storages = await storage_repo.get_all_storages(session=session)

    return all_storages


@storage_router.get(
    "/storage/{storage_id}",
    response_model=StorageSchema,
    status_code=status.HTTP_200_OK
)
async def get_storage_by_id(
        storage_id: int,
) -> StorageSchema:
    try:
        async with database.session() as session:
            storage = await storage_repo.get_storage_by_id(session=session, storage_id=storage_id)
    except StorageNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return storage


@storage_router.post("/add_storage", response_model=StorageSchema, status_code=status.HTTP_201_CREATED)
async def add_storage(
        storage_dto: StorageCreateUpdateSchema,
        current_user: UserSchema = Depends(get_current_user),
) -> StorageSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_storage = await storage_repo.create_storage(session=session, storage=storage_dto)
    except StorageAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_storage


@storage_router.put(
    "/update_storage/{storage_id}",
    response_model=StorageSchema,
    status_code=status.HTTP_200_OK,
)
async def update_storage(
        storage_id: int,
        storage_dto: StorageCreateUpdateSchema,
        current_user: UserSchema = Depends(get_current_user),
) -> StorageSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_storage = await storage_repo.update_storage(
                session=session,
                storage_id=storage_id,
                storage=storage_dto,
            )
    except StorageNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_storage


@storage_router.delete("/delete_storage/{storage_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_storage(
        storage_id: int,
        current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            storage = await storage_repo.delete_storage(session=session, storage_id=storage_id)
    except StorageNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return storage
