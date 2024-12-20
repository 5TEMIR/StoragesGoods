from pydantic import BaseModel, ConfigDict


class StorageCreateUpdateSchema(BaseModel):
    name: str
    address: str


class StorageSchema(StorageCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
