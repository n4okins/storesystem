import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class Item(BaseModel):
    item_name: str
    item_quantity: int
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4)


class ParchaseLog(BaseModel):
    item_id: uuid.UUID
    item_quantity: int
    created_at: datetime = Field(default_factory=datetime.now)


class RestockLog(BaseModel):
    user_id: uuid.UUID
    item_id: uuid.UUID
    item_quantity: int
    created_at: datetime = Field(default_factory=datetime.now)
