from pydantic import BaseModel, ConfigDict


class GoodsGroupCreateUpdateSchema(BaseModel):
    name: str
    description: str | None = None


class GoodsGroupSchema(GoodsGroupCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
