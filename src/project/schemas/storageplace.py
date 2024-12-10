from pydantic import BaseModel, ConfigDict


class StoragePlaceCreateUpdateSchema(BaseModel):
    good_id: int
    quantity: int
    storage_id: int


class StoragePlaceSchema(StoragePlaceCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
