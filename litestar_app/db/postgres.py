import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv
from pydantic import UUID4

from schemes import User

load_dotenv(dotenv_path='./.env')


class PostgresDB:
    def __init__(self):
        self.dsn = {
            'host': os.getenv('POSTGRES_HOST'),
            'port': os.getenv('POSTGRES_PORT'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'database': os.getenv('POSTGRES_DB'),
        }
        self.pool = None

    async def create_pool(self, min_size: int = 2, max_size: int = 4) -> None:
        if not self.pool:
            self.pool = await asyncpg.create_pool(**self.dsn, min_size=min_size, max_size=max_size)

    async def get_user(self, user_id: UUID4) -> dict | None:
        await self.create_pool()
        user = await self.pool.fetchrow('SELECT * FROM users WHERE uuid = $1', user_id)
        return user or None

    async def add_user(self, user: User) -> dict | None:
        await self.create_pool()
        async with self.pool.acquire() as conn:
            uuid = await conn.fetchval(
                'INSERT INTO users(full_name, phone) VALUES($1, $2) RETURNING uuid', user.full_name, user.phone
            )
        return await self.get_user(uuid) if uuid else None

    async def update_user(self, user: User, user_id: UUID4) -> dict | None:
        await self.create_pool()
        async with self.pool.acquire() as conn:
            uuid = await conn.fetchval(
                'UPDATE users SET full_name = $1, phone = $2, updated_at = $3 WHERE uuid = $4 RETURNING uuid',
                user.full_name,
                user.phone,
                datetime.now(),
                user_id,
            )
        return await self.get_user(uuid) if uuid else None

    async def delete_user(self, user_id: UUID4) -> str | None:
        await self.create_pool()
        async with self.pool.acquire() as conn:
            delete_user_id = await conn.fetchval('DELETE FROM users WHERE uuid = $1 RETURNING uuid', user_id)
        return delete_user_id or None
