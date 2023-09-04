import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from routers import router
from settings import settings

app = FastAPI(
    title='FastAPI',
    version='1.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.app_host,
        port=int(settings.app_port),
        log_level=settings.log_level,
    )
