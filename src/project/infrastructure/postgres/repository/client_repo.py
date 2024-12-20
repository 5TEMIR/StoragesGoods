from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.client import ClientSchema, ClientCreateUpdateSchema
from project.infrastructure.postgres.models import Client

from project.core.exceptions import ClientNotFound, ClientAlreadyExists


class ClientRepository:
    _collection: Type[Client] = Client

    async def get_all_clients(self, session: AsyncSession) -> list[ClientSchema]:
        query = select(self._collection)
        clients = await session.scalars(query)
        return [ClientSchema.model_validate(obj=client) for client in clients.all()]

    async def get_client_by_id(self, session: AsyncSession, client_id: int) -> ClientSchema:
        query = select(self._collection).where(self._collection.id == client_id)
        client = await session.scalar(query)
        if not client:
            raise ClientNotFound(_id=client_id)
        return ClientSchema.model_validate(obj=client)

    async def create_client(self, session: AsyncSession, client: ClientCreateUpdateSchema) -> ClientSchema:
        query = insert(self._collection).values(client.model_dump()).returning(self._collection)
        try:
            created_client = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise ClientAlreadyExists(name=client.name)
        return ClientSchema.model_validate(obj=created_client)

    async def update_client(self, session: AsyncSession, client_id: int,
                            client: ClientCreateUpdateSchema) -> ClientSchema:
        query = update(self._collection).where(self._collection.id == client_id).values(client.model_dump()).returning(
            self._collection)
        updated_client = await session.scalar(query)
        if not updated_client:
            raise ClientNotFound(_id=client_id)
        return ClientSchema.model_validate(obj=updated_client)

    async def delete_client(self, session: AsyncSession, client_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == client_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ClientNotFound(_id=client_id)
