from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, client_repo, get_current_user, check_for_admin_access
from project.schemas.client import *
from project.core.exceptions import *

client_router = APIRouter()


@client_router.get(
    "/all_clients",
    response_model=list[ClientSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_clients() -> list[ClientSchema]:
    async with database.session() as session:
        all_clients = await client_repo.get_all_clients(session=session)
    return all_clients


@client_router.get(
    "/client/{client_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK
)
async def get_client_by_id(client_id: int) -> ClientSchema:
    try:
        async with database.session() as session:
            client = await client_repo.get_client_by_id(session=session, client_id=client_id)
    except ClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return client


@client_router.post("/add_client", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def add_client(client_dto: ClientCreateUpdateSchema,
                     current_user: UserSchema = Depends(get_current_user), ) -> ClientSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_client = await client_repo.create_client(session=session, client=client_dto)
    except ClientAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_client


@client_router.put(
    "/update_client/{client_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK,
)
async def update_client(client_id: int, client_dto: ClientCreateUpdateSchema,
                        current_user: UserSchema = Depends(get_current_user), ) -> ClientSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_client = await client_repo.update_client(
                session=session,
                client_id=client_id,
                client=client_dto,
            )
    except ClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_client


@client_router.delete("/delete_client/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, current_user: UserSchema = Depends(get_current_user), ) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            client = await client_repo.delete_client(session=session, client_id=client_id)
    except ClientNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return client
