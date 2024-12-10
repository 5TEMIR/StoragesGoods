from fastapi import APIRouter, HTTPException, status

from project.api.depends import database, storage_place_repo
from project.schemas.storageplace import *
from project.core.exceptions import *

storage_place_router = APIRouter()


@storage_place_router.get(
    "/all_storage_places",
    response_model=list[StoragePlaceSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_storage_places() -> list[StoragePlaceSchema]:
    async with database.session() as session:
        all_places = await storage_place_repo.get_all_storage_places(session=session)
    return all_places


@storage_place_router.get(
    "/storage_place/{place_id}",
    response_model=StoragePlaceSchema,
    status_code=status.HTTP_200_OK
)
async def get_storage_place_by_id(place_id: int) -> StoragePlaceSchema:
    try:
        async with database.session() as session:
            place = await storage_place_repo.get_storage_place_by_id(session=session, place_id=place_id)
    except StoragePlaceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return place


@storage_place_router.post("/add_storage_place", response_model=StoragePlaceSchema, status_code=status.HTTP_201_CREATED)
async def add_storage_place(storage_place_dto: StoragePlaceCreateUpdateSchema) -> StoragePlaceSchema:
    try:
        async with database.session() as session:
            new_place = await storage_place_repo.create_storage_place(session=session, storage_place=storage_place_dto)
    except StoragePlaceAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_place


@storage_place_router.put(
    "/update_storage_place/{place_id}",
    response_model=StoragePlaceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_storage_place(place_id: int, storage_place_dto: StoragePlaceCreateUpdateSchema) -> StoragePlaceSchema:
    try:
        async with database.session() as session:
            updated_place = await storage_place_repo.update_storage_place(
                session=session,
                place_id=place_id,
                storage_place=storage_place_dto,
            )
    except StoragePlaceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_place


@storage_place_router.delete("/delete_storage_place/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_storage_place(place_id: int) -> None:
    try:
        async with database.session() as session:
            storageplace = await storage_place_repo.delete_storage_place(session=session, place_id=place_id)
    except StoragePlaceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return storageplace
