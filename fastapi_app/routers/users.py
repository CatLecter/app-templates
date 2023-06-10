from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import UUID4

from schemes.users import ResponseUser, User

router = APIRouter(prefix='/user', tags=['Users'])


@router.get(path='/{user_id}', response_model=ResponseUser)
async def get_user(user_id: UUID4, request: Request) -> ResponseUser:
    user = await request.state.db.get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User with UUID={user_id} not found')
    return user


@router.post(path='/', response_model=ResponseUser)
async def post_user(item: User, request: Request) -> ResponseUser:
    user = await request.state.db.add_user(user=item)
    if not user:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Failed to create user')
    return user


@router.put(path='/{user_id}', response_model=ResponseUser)
async def put_user(user_id: UUID4, item: User, request: Request) -> ResponseUser:
    user = await request.state.db.update_user(user=item, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'User with UUID={user_id} has not been updated',
        )
    return user


@router.delete(path='/{user_id}', response_class=JSONResponse)
async def delete_user(user_id: UUID4, request: Request) -> JSONResponse:
    id_deleted_user = await request.state.db.delete_user(user_id=user_id)
    if not id_deleted_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User with UUID={user_id} not found')
    return JSONResponse(content={'result': 'successful', 'message': f'User with UUID={id_deleted_user}'})
