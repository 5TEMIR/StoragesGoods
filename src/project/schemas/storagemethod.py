from pydantic import BaseModel, ConfigDict


class StorageMethodCreateUpdateSchema(BaseModel):
    name: str
    description: str | None = None


class StorageMethodSchema(StorageMethodCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
