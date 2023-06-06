from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import UUID4

from db.postgres import PostgresDB
from dependencies.db import deps
from schemes.users import ResponseUser, User

router = APIRouter(prefix='/user', tags=['Users'])


@router.get(
    path='/{user_id}',
    response_model=ResponseUser,
)
async def get_user(
        user_id: UUID4,
        db: PostgresDB = deps.depends(PostgresDB)
) -> ResponseUser:
    user = db.get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with UUID={user_id} not found'
        )
    return ResponseUser(**user)


@router.post(
    path='/',
    response_model=ResponseUser
)
async def post_user(
        item: User,
        db: PostgresDB = deps.depends(PostgresDB)
) -> ResponseUser:
    user = db.add_user(user=item)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={'result': 'failed', 'detail': f'Failed to create user'},
        )
    return ResponseUser(**user)


@router.put(
    path='/{user_id}',
    response_model=ResponseUser,
)
async def put_user(
        user_id: UUID4,
        item: User,
        db: PostgresDB = deps.depends(PostgresDB)
) -> ResponseUser:
    user = db.update_user(user=item, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={'result': 'failed', 'detail': f'User with UUID={user_id} has not been updated'},
        )
    return ResponseUser(**user)


@router.delete(
    path='/{user_id}',
    response_class=JSONResponse,
)
async def delete_user(
        user_id: UUID4,
        db: PostgresDB = deps.depends(PostgresDB)
) -> JSONResponse:
    delete_user_id = db.delete_user(user_id=user_id)
    if not delete_user_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={'result': 'failed', 'detail': f'User with UUID={user_id} not found'},
        )
    return JSONResponse(
        content={
            'result': 'successful',
            'detail': f'User with UUID={delete_user_id}'
        }
    )
