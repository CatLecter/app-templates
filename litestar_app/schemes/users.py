from datetime import datetime

import orjson
from pydantic import BaseModel, UUID4


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastJsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class User(FastJsonModel):
    full_name: str
    phone: str


class ResponseUser(User):
    uuid: UUID4
    created_at: datetime
    updated_at: datetime
