from pydantic import BaseModel, UUID4
from datetime import datetime


class User(BaseModel):
    full_name: str
    phone: str


class ResponseUser(User):
    uuid: UUID4
    created_at: datetime
    updated_at: datetime
