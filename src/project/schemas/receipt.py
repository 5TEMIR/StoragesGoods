from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReceiptCreateUpdateSchema(BaseModel):
    receip_date: datetime
    supplier_id: int


class ReceiptSchema(ReceiptCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
