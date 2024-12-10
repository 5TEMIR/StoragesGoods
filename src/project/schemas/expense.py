from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ExpenseCreateUpdateSchema(BaseModel):
    expens_date: datetime
    client_id: int


class ExpenseSchema(ExpenseCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
