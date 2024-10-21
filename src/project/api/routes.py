from fastapi import APIRouter

from project.infrastructure.postgres.repository.storage_repo import StorageRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.storage import StorageSchema


router = APIRouter()


@router.get("/all_storages", response_model=list[StorageSchema])
async def get_all_storages() -> list[StorageSchema]:
    storage_repo = StorageRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await storage_repo.check_connection(session=session)
        all_storages = await storage_repo.get_all_storages(session=session)

    return all_storages
