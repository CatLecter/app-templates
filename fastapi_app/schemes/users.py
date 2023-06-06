from datetime import datetime

from pydantic import BaseModel, UUID4


class User(BaseModel):
    full_name: str
    phone: str


class ResponseUser(User):
    uuid: UUID4
    created_at: datetime
    updated_at: datetime
