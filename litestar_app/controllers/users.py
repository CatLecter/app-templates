from litestar import post, get, put, delete
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK
from pydantic import UUID4

from db.postgres import PostgresDB
from schemes import User, ResponseUser

db = PostgresDB()


class UserController(Controller):
    path = '/user'

    @get(path='/{user_id:uuid}')
    async def get_user(self, user_id: UUID4) -> ResponseUser:
        user = await db.get_user(user_id)
        return ResponseUser(
            uuid=user.get('uuid'),
            full_name=user.get('full_name'),
            phone=user.get('phone'),
            created_at=user.get('created_at'),
            updated_at=user.get('updated_at'),
        )

    @post()
    async def add_user(self, data: User) -> ResponseUser:
        user_id = await db.add_user(data)
        user = await db.get_user(user_id)
        return ResponseUser(
            uuid=user.get('uuid'),
            full_name=user.get('full_name'),
            phone=user.get('phone'),
            created_at=user.get('created_at'),
            updated_at=user.get('updated_at'),
        )

    @put()
    async def change_user(self, user_id: UUID4, data: User) -> ResponseUser:
        user_id = await db.update_user(data, user_id)
        user = await db.get_user(user_id)
        return ResponseUser(
            uuid=user.get('uuid'),
            full_name=user.get('full_name'),
            phone=user.get('phone'),
            created_at=user.get('created_at'),
            updated_at=user.get('updated_at'),
        )

    @delete(path='/{user_id:uuid}', status_code=HTTP_200_OK)
    async def delete_user(self, user_id: UUID4) -> dict:
        user_id = await db.delete_user(user_id)
        return {'result': 'successful', 'detail': f'User with UUID={user_id} deleted'}
