import os
from datetime import datetime
from uuid import UUID

import asyncpg
from dotenv import load_dotenv
from schemes.users import User

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

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(**self.dsn, min_size=2, max_size=4)

    async def get_user(self, user_id: UUID):
        if not self.pool:
            await self.create_pool()
        user = await self.pool.fetchrow('SELECT * FROM users WHERE uuid = $1', user_id)
        return user

    async def add_user(self, user: User):
        if not self.pool:
            await self.create_pool()
        async with self.pool.acquire() as conn:
            user_id = await conn.fetchval(
                'INSERT INTO users(full_name, phone) VALUES($1, $2) RETURNING uuid', user.full_name, user.phone
            )
        return user_id

    async def update_user(self, user: User, user_id: UUID):
        if not self.pool:
            await self.create_pool()
        async with self.pool.acquire() as conn:
            uuid = await conn.fetchval(
                'UPDATE users SET full_name = $1, phone = $2, updated_at = $3 WHERE uuid = $4 RETURNING uuid',
                user.full_name,
                user.phone,
                datetime.now(),
                user_id,
            )
        return uuid

    async def delete_user(self, user_id: UUID):
        if not self.pool:
            await self.create_pool()
        async with self.pool.acquire() as conn:
            user_id = await conn.fetchval('DELETE FROM users WHERE uuid = $1 RETURNING uuid', user_id)
        return user_id
