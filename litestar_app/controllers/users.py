from litestar import post, get, put, delete
from litestar.controller import Controller
from litestar.di import Provide
from litestar.enums import MediaType
from litestar.response import Response
from litestar.status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from pydantic import UUID4

from db.postgres import provides_postgres, PostgresDB
from schemes import User, ResponseUser


class UserController(Controller):
    path = '/user'
    tags = ['Users']
    dependencies = {"db": Provide(provides_postgres)}

    @get(path='/{user_id:uuid}', status_code=HTTP_200_OK)
    async def get_user(self, db: PostgresDB, user_id: UUID4) -> Response[ResponseUser | dict]:
        user = await db.get_user(user_id)
        return Response(
            content=ResponseUser(
                uuid=str(user.get('uuid')),
                full_name=user.get('full_name'),
                phone=user.get('phone'),
                created_at=user.get('created_at'),
                updated_at=user.get('updated_at'),
            ) if user else {'result': 'Not Found', 'detail': f'User with UUID={user_id} not found'},
            status_code=HTTP_200_OK if user else HTTP_404_NOT_FOUND,
            media_type=MediaType.JSON,
        )

    @post(path='/', status_code=HTTP_200_OK)
    async def add_user(self, db: PostgresDB, data: User) -> Response[ResponseUser | dict]:
        user = await db.add_user(data)
        return Response(
            content=ResponseUser(
                uuid=str(user.get('uuid')),
                full_name=user.get('full_name'),
                phone=user.get('phone'),
                created_at=user.get('created_at'),
                updated_at=user.get('updated_at'),
            ) if user else {'result': 'Internal Server Error', 'detail': 'Failed to create user'},
            status_code=HTTP_200_OK if user else HTTP_500_INTERNAL_SERVER_ERROR,
            media_type=MediaType.JSON,
        )

    @put()
    async def change_user(self, db: PostgresDB, user_id: UUID4, data: User) -> Response[ResponseUser | dict]:
        user = await db.update_user(data, user_id)
        return Response(
            content=ResponseUser(
                uuid=str(user.get('uuid')),
                full_name=user.get('full_name'),
                phone=user.get('phone'),
                created_at=user.get('created_at'),
                updated_at=user.get('updated_at'),
            ) if user else {'result': 'Internal Server Error', 'detail': 'Failed to update user'},
            status_code=HTTP_200_OK if user else HTTP_500_INTERNAL_SERVER_ERROR,
            media_type=MediaType.JSON,
        )

    @delete(path='/{user_id:uuid}', status_code=HTTP_200_OK)
    async def delete_user(self, db: PostgresDB, user_id: UUID4) -> Response[dict]:
        delete_user_id = await db.delete_user(user_id)
        return Response(
            content={
                'result': 'Successful', 'detail': f'User with UUID={delete_user_id} deleted'
            } if delete_user_id else {
                'result': 'Not Found', 'detail': f'User with UUID={user_id} not found'
            },
            status_code=HTTP_200_OK if delete_user_id else HTTP_404_NOT_FOUND,
            media_type=MediaType.JSON,
        )
