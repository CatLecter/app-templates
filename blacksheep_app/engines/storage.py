from datetime import datetime
from uuid import UUID

import asyncpg
from schemes.users import RespUser, User
from settings import settings


class DBEngine:
    def __init__(self):
        self.host = settings.pg_host
        self.port = settings.pg_port
        self.user = settings.pg_user
        self.password = settings.pg_password
        self.database = settings.pg_db
        self.pool = {}

    async def create_pool(self, min_size: int = 1, max_size: int = 50) -> None:
        if self.pool.get('pool') is None:
            self.pool['pool'] = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                min_size=min_size,
                max_size=max_size,
            )

    async def get_user(self, user_id: UUID) -> RespUser | None:
        await self.create_pool()
        async with self.pool['pool'].acquire() as conn:
            user = await conn.fetchrow('SELECT * FROM users WHERE uuid = $1', user_id)
        return RespUser(**user) if user else None

    async def add_user(self, user: User) -> RespUser | None:
        await self.create_pool()
        async with self.pool['pool'].acquire() as conn:
            user_id = await conn.fetchval(
                'INSERT INTO users(full_name, phone) VALUES($1, $2) RETURNING uuid', user.full_name, user.phone
            )
        return None if not user_id else await self.get_user(user_id)

    async def update_user(self, user: User, user_id: UUID) -> RespUser | None:
        await self.create_pool()
        async with self.pool['pool'].acquire() as conn:
            user_id = await conn.fetchval(
                'UPDATE users SET full_name = $1, phone = $2, updated_at = $3 WHERE uuid = $4 RETURNING uuid',
                user.full_name,
                user.phone,
                datetime.now(),
                user_id,
            )
        return None if not user_id else await self.get_user(user_id)

    async def delete_user(self, user_id: UUID) -> str | None:
        await self.create_pool()
        async with self.pool['pool'].acquire() as conn:
            result = await conn.fetchrow('DELETE FROM users WHERE uuid = $1 RETURNING uuid', user_id)
        return result['uuid'] if result else None

    async def close_pool(self) -> None:
        if self.pool.get('pool') is not None:
            await self.pool['pool'].close()

    async def __call__(self, *args, **kwargs):
        await self.create_pool()
