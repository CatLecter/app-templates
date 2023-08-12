from datetime import datetime

from pydantic import UUID4, BaseModel


class User(BaseModel):
    full_name: str
    phone: str


class ResponseUser(User):
    uuid: UUID4
    created_at: datetime
    updated_at: datetime
