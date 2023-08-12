from http import HTTPStatus
from typing import Any

from fastapi import HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from models.base import Base
from settings import settings


class ORMEngine:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=settings.storage_uri, echo=False, echo_pool=True, pool_size=50, max_overflow=10
        )
        self.async_session = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
        )

    async def execute(self, stmt: Base) -> Any:
        try:
            async with self.async_session() as session:
                cursor = await session.execute(stmt)
                await session.commit()
                result = cursor.fetchone()
                return result[0] if result else None
        except OperationalError as error:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error)
        finally:
            await session.close()
