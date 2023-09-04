from uuid import UUID

from dependencies.storage import provides_postgres
from engines.storage import DBEngine
from litestar import delete, get, post, put
from litestar.controller import Controller
from litestar.di import Provide
from litestar.enums import MediaType
from litestar.response import Response
from litestar.status_codes import (HTTP_200_OK, HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from schemes import ResponseUser, User


class UserController(Controller):
    path = '/user'
    tags = ['Users']
    dependencies = {'db': Provide(dependency=provides_postgres, use_cache=True)}

    @get(path='/{user_id:uuid}', status_code=HTTP_200_OK)
    async def get_user(self, db: DBEngine, user_id: UUID) -> Response[ResponseUser | dict]:
        user = await db.get_user(user_id)
        return Response(
            content=user if user else {'result': 'failed', 'detail': f'User with UUID={user_id} not found'},
            status_code=HTTP_200_OK if user else HTTP_404_NOT_FOUND,
            media_type=MediaType.JSON,
        )

    @post(path='/', status_code=HTTP_200_OK)
    async def add_user(self, db: DBEngine, data: User) -> Response[ResponseUser | dict]:
        user = await db.add_user(data)
        return Response(
            content=user if user else {'result': 'failed', 'detail': 'Failed to create user'},
            status_code=HTTP_200_OK if user else HTTP_500_INTERNAL_SERVER_ERROR,
            media_type=MediaType.JSON,
        )

    @put()
    async def put_user(self, db: DBEngine, user_id: UUID, data: User) -> Response[ResponseUser | dict]:
        user = await db.update_user(data, user_id)
        return Response(
            content=user if user else {'result': 'failed', 'detail': f'User with UUID={user_id} not found'},
            status_code=HTTP_200_OK if user else HTTP_500_INTERNAL_SERVER_ERROR,
            media_type=MediaType.JSON,
        )

    @delete(path='/{user_id:uuid}', status_code=HTTP_200_OK)
    async def delete_user(self, db: DBEngine, user_id: UUID) -> Response[dict]:
        delete_user_id = await db.delete_user(user_id)
        return Response(
            content=(
                {'result': 'successful', 'detail': f'User with UUID={delete_user_id} deleted'}
                if delete_user_id
                else {'result': 'failed', 'detail': f'User with UUID={user_id} not found'}
            ),
            status_code=HTTP_200_OK if delete_user_id else HTTP_404_NOT_FOUND,
            media_type=MediaType.JSON,
        )
