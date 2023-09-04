import uvicorn
from controllers import routes
from litestar import Litestar
from settings import settings

app = Litestar(route_handlers=[*routes])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.app_host,
        port=int(settings.app_port),
        log_level=settings.log_level,
        reload=settings.reload,
    )
