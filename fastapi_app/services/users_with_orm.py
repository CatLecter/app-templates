from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, insert, update
from sqlalchemy.future import select

from dependencies import container
from engines.storage_with_orm import ORMEngine
from models.users import User as UserModel
from schemes.users import ResponseUser, User


class UserWithORMService:
    def __init__(self):
        self.db: ORMEngine = container.resolve(ORMEngine)

    async def get_user_by_uuid(self, user_uuid: UUID) -> ResponseUser | None:
        stmt = select(UserModel).where(UserModel.uuid == user_uuid)
        user: UserModel | None = await self.db.execute(stmt)
        return ResponseUser(**user.__dict__) if user else None

    async def add_user(self, user: User) -> ResponseUser | None:
        stmt = insert(UserModel).values(full_name=user.full_name, phone=user.phone).returning(UserModel.uuid)
        user_uuid = await self.db.execute(stmt)
        user = await self.get_user_by_uuid(user_uuid)
        return user

    async def update_user(self, user: User, user_uuid: UUID) -> ResponseUser | None:
        stmt = (
            update(UserModel)
            .values(full_name=user.full_name, phone=user.full_name, updated_at=datetime.now())
            .where(UserModel.uuid == user_uuid)
            .returning(UserModel.uuid)
        )
        user_uuid = await self.db.execute(stmt)
        user = await self.get_user_by_uuid(user_uuid)
        return user

    async def delete_user(self, user_uuid: UUID) -> bool:
        stmt = delete(UserModel).where(UserModel.uuid == user_uuid).returning(UserModel.uuid)
        user_uuid = await self.db.execute(stmt)
        return True if user_uuid else False


container.register(obj_type=UserWithORMService, instance=UserWithORMService())
