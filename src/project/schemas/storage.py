from pydantic import BaseModel, Field, ConfigDict


class StorageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
