import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from db.postgres import PostgresDB
from routers import router
from settings import settings


def create_app() -> FastAPI:
    application = FastAPI(
        title='FastAPI',
        version='1.0',
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
    )

    db = PostgresDB()

    @application.on_event("startup")
    async def startup():
        await db.create_pool()

    @application.on_event("shutdown")
    async def shutdown():
        await db.close_pool()

    @application.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.db = db
        return await call_next(request)

    application.include_router(router)

    return application


app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.app_host,
        port=int(settings.app_port),
        log_level=settings.log_level,
    )
