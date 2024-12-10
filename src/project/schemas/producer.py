from pydantic import BaseModel, ConfigDict


class ProducerCreateUpdateSchema(BaseModel):
    name: str
    address: str | None = None


class ProducerSchema(ProducerCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
