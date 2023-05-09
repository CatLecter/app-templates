from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    __slots__ = ('full_name', 'phone')

    full_name: str
    phone: str


@dataclass
class RespUser(User):
    __slots__ = ('full_name', 'phone', 'uuid', 'created_at', 'updated_at')

    uuid: UUID
    created_at: datetime
    updated_at: datetime
