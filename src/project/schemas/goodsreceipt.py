from pydantic import BaseModel, ConfigDict


class GoodsReceiptSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    receipt_id: int
    storage_place_id: int
    quantity: int