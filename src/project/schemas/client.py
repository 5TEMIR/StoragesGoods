from pydantic import BaseModel, ConfigDict


class ClientCreateUpdateSchema(BaseModel):
    name: str
    address: str | None = None


class ClientSchema(ClientCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
