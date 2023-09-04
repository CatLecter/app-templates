from fastapi import APIRouter
from routers.users import router as users_router
from routers.users_with_orm import router as user_with_orm_router

router = APIRouter(prefix='/api')
router.include_router(users_router)
router.include_router(user_with_orm_router)
