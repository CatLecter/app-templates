from uuid import UUID

from db.postgres import PostgresDB
from schemes.users import RespUser, User

from blacksheep.server.bindings import FromJson, FromQuery
from blacksheep.server.controllers import ApiController, delete, get, post, put

db = PostgresDB()


class UserController(ApiController):
    @classmethod
    def route(cls) -> str:
        return 'user'

    @get()
    async def get_item(self, user_id: FromQuery[UUID]) -> RespUser:
        user = await db.get_user(user_id.value)
        return RespUser(
            uuid=user.get('uuid'),
            full_name=user.get('full_name'),
            phone=user.get('phone'),
            created_at=user.get('created_at'),
            updated_at=user.get('updated_at'),
        )

    @post()
    async def post_item(self, response: FromJson[User]) -> RespUser:
        user_id = await db.add_user(response.value)
        user = await db.get_user(user_id)
        return RespUser(
            uuid=user.get('uuid'),
            full_name=user.get('full_name'),
            phone=user.get('phone'),
            created_at=user.get('created_at'),
            updated_at=user.get('updated_at'),
        )

    @put()
    async def put_item(self, response: FromJson[User], user_id: FromQuery[UUID]) -> RespUser:
        user_id = await db.update_user(response.value, user_id.value)
        user = await db.get_user(user_id)
        return RespUser(
            uuid=user.get('uuid'),
            full_name=user.get('full_name'),
            phone=user.get('phone'),
            created_at=user.get('created_at'),
            updated_at=user.get('updated_at'),
        )

    @delete()
    async def delete_item(self, user_id: FromQuery[UUID]) -> dict:
        user_id = await db.delete_user(user_id.value)
        return {'result': 'successful', 'detail': f'User with UUID={user_id} deleted'}
