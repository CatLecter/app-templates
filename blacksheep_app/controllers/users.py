from http import HTTPStatus
from uuid import UUID

from blacksheep import FromJSON, FromQuery, Response, json
from blacksheep.server.controllers import ApiController, delete, get, post, put

from db.postgres import PostgresDB
from schemes.users import RespUser, User


class UserController(ApiController):
    @classmethod
    def route(cls) -> str:
        return 'user'

    @classmethod
    def version(cls) -> str:
        return 'v1'

    @classmethod
    def class_name(cls) -> str:
        return 'Users'

    @get()
    async def get_user(self, db: PostgresDB, user_id: FromQuery[UUID]) -> Response:
        user = await db.get_user(user_id.value)
        if not user:
            return json(
                data={'result': 'failed', 'detail': f'User with UUID={user_id.value} not found'},
                status=HTTPStatus.NOT_FOUND,
            )
        return json(data=RespUser(**user), status=HTTPStatus.OK)

    @post()
    async def post_user(self, db: PostgresDB, response: FromJSON[User]) -> Response:
        user = await db.add_user(response.value)
        if not user:
            return json(
                data={'result': 'failed', 'detail': f'Failed to create user'}, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return json(data=RespUser(**user), status=HTTPStatus.OK)

    @put()
    async def put_user(self, db: PostgresDB, response: FromJSON[User], user_id: FromQuery[UUID]) -> Response:
        user = await db.update_user(response.value, user_id.value)
        if not user:
            return json(
                data={'result': 'failed', 'detail': f'User with UUID={user_id.value} has not been updated'},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        return json(data=RespUser(**user), status=HTTPStatus.OK)

    @delete()
    async def delete_user(self, db: PostgresDB, user_id: FromQuery[UUID]) -> Response:
        delete_user_id = await db.delete_user(user_id.value)
        if not delete_user_id:
            return json(
                data={'result': 'failed', 'detail': f'User with UUID={user_id.value} not found'},
                status=HTTPStatus.NOT_FOUND,
            )
        return json(
            data={'result': 'successful', 'detail': f'User with UUID={delete_user_id} deleted'}, status=HTTPStatus.OK
        )
