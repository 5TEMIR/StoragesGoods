from pydantic import BaseModel, ConfigDict


class GoodCreateUpdateSchema(BaseModel):
    name: str
    description: str | None = None
    goods_group_id: int
    producer_id: int
    totalquantity: int
    storage_method_id: int


class GoodSchema(GoodCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
