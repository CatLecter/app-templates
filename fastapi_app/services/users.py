from datetime import datetime
from uuid import UUID

from dependencies import container
from engines.storage import DBEngine
from schemes.users import ResponseUser, User


class UserService:
    def __init__(self):
        self.db: DBEngine = container.resolve(DBEngine)

    async def get_user_by_uuid(self, user_uuid: UUID) -> ResponseUser | None:
        user = await self.db.fetchrow('SELECT * FROM users WHERE uuid = $1', str(user_uuid))
        return ResponseUser(**user) if user else None

    async def add_user(self, user: User) -> ResponseUser | None:
        user_uuid: UUID = await self.db.fetchval(
            'INSERT INTO users(full_name, phone) VALUES($1, $2) RETURNING uuid', user.full_name, user.phone
        )
        return None if not user_uuid else await self.get_user_by_uuid(user_uuid)

    async def update_user(self, user: User, user_uuid: UUID) -> ResponseUser | None:
        _user_uuid: UUID = await self.db.fetchval(
            'UPDATE users SET full_name = $1, phone = $2, updated_at = $3 WHERE uuid = $4 RETURNING uuid',
            user.full_name,
            user.phone,
            datetime.now(),
            str(user_uuid),
        )
        return None if not _user_uuid else await self.get_user_by_uuid(_user_uuid)

    async def delete_user(self, user_uuid: UUID) -> bool:
        result: dict | None = await self.db.fetchrow('DELETE FROM users WHERE uuid = $1 RETURNING uuid', str(user_uuid))
        if not result:
            return False
        return True if result.get('uuid') else False


container.register(obj_type=UserService, instance=UserService())
