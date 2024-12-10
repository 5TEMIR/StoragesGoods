from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from sqlalchemy.exc import IntegrityError

from project.schemas.producer import ProducerSchema, ProducerCreateUpdateSchema
from project.infrastructure.postgres.models import Producer

from project.core.exceptions import ProducerNotFound, ProducerAlreadyExists


class ProducerRepository:
    _collection: Type[Producer] = Producer

    async def get_all_producers(self, session: AsyncSession) -> list[ProducerSchema]:
        query = select(self._collection)
        producers = await session.scalars(query)
        return [ProducerSchema.model_validate(obj=producer) for producer in producers.all()]

    async def get_producer_by_id(self, session: AsyncSession, producer_id: int) -> ProducerSchema:
        query = select(self._collection).where(self._collection.id == producer_id)
        producer = await session.scalar(query)
        if not producer:
            raise ProducerNotFound(_id=producer_id)
        return ProducerSchema.model_validate(obj=producer)

    async def create_producer(self, session: AsyncSession, producer: ProducerCreateUpdateSchema) -> ProducerSchema:
        query = insert(self._collection).values(producer.model_dump()).returning(self._collection)
        try:
            created_producer = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise ProducerAlreadyExists(name=producer.name)
        return ProducerSchema.model_validate(obj=created_producer)

    async def update_producer(self, session: AsyncSession, producer_id: int,
                              producer: ProducerCreateUpdateSchema) -> ProducerSchema:
        query = update(self._collection).where(self._collection.id == producer_id).values(
            producer.model_dump()).returning(self._collection)
        updated_producer = await session.scalar(query)
        if not updated_producer:
            raise ProducerNotFound(_id=producer_id)
        return ProducerSchema.model_validate(obj=updated_producer)

    async def delete_producer(self, session: AsyncSession, producer_id: int) -> None:
        query = delete(self._collection).where(self._collection.id == producer_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise ProducerNotFound(_id=producer_id)
