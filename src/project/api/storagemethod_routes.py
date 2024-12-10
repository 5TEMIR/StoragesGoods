from fastapi import APIRouter, HTTPException, status

from project.api.depends import database, storage_method_repo
from project.schemas.storagemethod import *
from project.core.exceptions import *

storage_method_router = APIRouter()


@storage_method_router.get(
    "/all_storage_methods",
    response_model=list[StorageMethodSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_storage_methods() -> list[StorageMethodSchema]:
    async with database.session() as session:
        all_storage_methods = await storage_method_repo.get_all_storage_methods(session=session)
    return all_storage_methods


@storage_method_router.get(
    "/storage_method/{storage_method_id}",
    response_model=StorageMethodSchema,
    status_code=status.HTTP_200_OK
)
async def get_storage_method_by_id(storage_method_id: int) -> StorageMethodSchema:
    try:
        async with database.session() as session:
            storage_method = await storage_method_repo.get_storage_method_by_id(session=session,
                                                                                storage_method_id=storage_method_id)
    except StorageMethodNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return storage_method


@storage_method_router.post("/add_storage_method", response_model=StorageMethodSchema,
                            status_code=status.HTTP_201_CREATED)
async def add_storage_method(storage_method_dto: StorageMethodCreateUpdateSchema) -> StorageMethodSchema:
    try:
        async with database.session() as session:
            new_storage_method = await storage_method_repo.create_storage_method(session=session,
                                                                                 storage_method=storage_method_dto)
    except StorageMethodAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_storage_method


@storage_method_router.put(
    "/update_storage_method/{storage_method_id}",
    response_model=StorageMethodSchema,
    status_code=status.HTTP_200_OK,
)
async def update_storage_method(storage_method_id: int,
                                storage_method_dto: StorageMethodCreateUpdateSchema) -> StorageMethodSchema:
    try:
        async with database.session() as session:
            updated_storage_method = await storage_method_repo.update_storage_method(
                session=session,
                storage_method_id=storage_method_id,
                storage_method=storage_method_dto,
            )
    except StorageMethodNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_storage_method


@storage_method_router.delete("/delete_storage_method/{storage_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_storage_method(storage_method_id: int) -> None:
    try:
        async with database.session() as session:
            storagemethod = await storage_method_repo.delete_storage_method(session=session,
                                                                            storage_method_id=storage_method_id)
    except StorageMethodNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return storagemethod
