from pydantic import BaseModel, ConfigDict


class GoodsExpenseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    expense_id: int
    storage_place_id: int
    quantity: int
