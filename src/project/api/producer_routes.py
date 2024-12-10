from fastapi import APIRouter, HTTPException, status

from project.api.depends import database, producer_repo
from project.schemas.producer import *
from project.core.exceptions import *

producer_router = APIRouter()


@producer_router.get(
    "/all_producers",
    response_model=list[ProducerSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_producers() -> list[ProducerSchema]:
    async with database.session() as session:
        all_producers = await producer_repo.get_all_producers(session=session)
    return all_producers


@producer_router.get(
    "/producer/{producer_id}",
    response_model=ProducerSchema,
    status_code=status.HTTP_200_OK
)
async def get_producer_by_id(producer_id: int) -> ProducerSchema:
    try:
        async with database.session() as session:
            producer = await producer_repo.get_producer_by_id(session=session, producer_id=producer_id)
    except ProducerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return producer


@producer_router.post("/add_producer", response_model=ProducerSchema, status_code=status.HTTP_201_CREATED)
async def add_producer(producer_dto: ProducerCreateUpdateSchema) -> ProducerSchema:
    try:
        async with database.session() as session:
            new_producer = await producer_repo.create_producer(session=session, producer=producer_dto)
    except ProducerAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_producer


@producer_router.put(
    "/update_producer/{producer_id}",
    response_model=ProducerSchema,
    status_code=status.HTTP_200_OK,
)
async def update_producer(producer_id: int, producer_dto: ProducerCreateUpdateSchema) -> ProducerSchema:
    try:
        async with database.session() as session:
            updated_producer = await producer_repo.update_producer(
                session=session,
                producer_id=producer_id,
                producer=producer_dto,
            )
    except ProducerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_producer


@producer_router.delete("/delete_producer/{producer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producer(producer_id: int) -> None:
    try:
        async with database.session() as session:
            producer = await producer_repo.delete_producer(session=session, producer_id=producer_id)
    except ProducerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return producer
