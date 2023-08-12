from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import UUID4

from dependencies import container
from schemes.users import ResponseUser, User
from services.users_with_orm import UserWithORMService

router = APIRouter(prefix='/user/orm', tags=['Users with ORM'])


@router.post(path='/', response_model=ResponseUser)
async def add_user(item: User) -> ResponseUser:
    user_service: UserWithORMService = container.resolve(UserWithORMService)
    user = await user_service.add_user(item)
    if not user:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Failed to create user')
    return user


@router.get(path='/{user_id}', response_model=ResponseUser)
async def get_user_by_uuid(user_id: UUID4) -> ResponseUser:
    user_service: UserWithORMService = container.resolve(UserWithORMService)
    user = await user_service.get_user_by_uuid(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User with UUID={user_id} not found')
    return user


@router.put(path='/{user_id}', response_model=ResponseUser)
async def update_user(user_id: UUID4, item: User) -> ResponseUser:
    user_service: UserWithORMService = container.resolve(UserWithORMService)
    user: ResponseUser | None = await user_service.update_user(item, user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'User with UUID={user_id} has not been updated',
        )
    return user


@router.delete(path='/{user_id}', response_class=JSONResponse)
async def delete_user(user_id: UUID4) -> JSONResponse:
    user_service: UserWithORMService = container.resolve(UserWithORMService)
    is_deleted: bool = await user_service.delete_user(user_id)
    if not is_deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User with UUID={user_id} not found')
    return JSONResponse(content={'result': 'successful', 'message': f'User with UUID={user_id} deleted'})
