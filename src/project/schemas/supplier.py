from pydantic import BaseModel, ConfigDict


class SupplierCreateUpdateSchema(BaseModel):
    name: str
    address: str | None = None


class SupplierSchema(SupplierCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
