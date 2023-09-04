from datetime import datetime

from msgspec import Struct
from msgspec.inspect import UUIDType


class User(Struct):
    full_name: str
    phone: str


class ResponseUser(User):
    uuid: UUIDType
    created_at: datetime
    updated_at: datetime
