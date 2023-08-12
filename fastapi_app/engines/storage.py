from typing import Any

import asyncpg

from settings import settings


class DBEngine:
    def __init__(self) -> None:
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

    async def fetchrow(self, *args, **kwargs) -> Any:
        await self.create_pool()
        async with self.pool['pool'].acquire() as conn:
            result = await conn.fetchrow(*args, **kwargs)
        return result

    async def fetchval(self, *args, **kwargs) -> Any:
        await self.create_pool()
        async with self.pool['pool'].acquire() as conn:
            result = await conn.fetchval(*args, **kwargs)
        return result

    async def close_pool(self) -> None:
        if self.pool.get('pool') is not None:
            await self.pool['pool'].close()

    async def __call__(self, *args, **kwargs) -> None:
        await self.create_pool()
