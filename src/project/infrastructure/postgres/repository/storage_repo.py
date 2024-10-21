from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.storage import StorageSchema
from project.infrastructure.postgres.models import Storage

from project.core.config import settings


class StorageRepository:
    _collection: Type[Storage] = Storage

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_storages(
            self,
            session: AsyncSession,
    ) -> list[StorageSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.storages;"

        storages = await session.execute(text(query))

        return [StorageSchema.model_validate(obj=storage) for storage in storages.mappings().all()]
