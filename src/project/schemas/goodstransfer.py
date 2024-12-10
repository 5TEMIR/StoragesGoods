from pydantic import BaseModel, ConfigDict
from datetime import datetime


class GoodsTransferCreateUpdateSchema(BaseModel):
    transfer_date: datetime
    quantity: int
    from_storage_id: int
    to_storage_id: int
    good_id: int


class GoodsTransferSchema(GoodsTransferCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
