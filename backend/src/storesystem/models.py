import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    item_id: uuid.UUID
    item_name: Optional[str] = None
    item_quantity: int = Field(..., gt=0)


class LogBaseModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)

    def model_dump_for_log(self) -> dict:
        json = self.model_dump(mode="json")
        if "item_name" in json:
            json.pop("item_name")
        return json


class ParchaseLog(LogBaseModel):
    item_id: uuid.UUID
    item_quantity: int = Field(..., gt=0)


class RestockLog(LogBaseModel):
    user_id: uuid.UUID
    item_id: uuid.UUID
    item_quantity: int = Field(..., gt=0)
    item_name: Optional[str]
