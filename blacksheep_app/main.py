import uvicorn
from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from controllers import UserController  # noqa
from db.postgres import PostgresDB
from settings import settings

app = Application()
app.services.add_instance(PostgresDB())

docs = OpenAPIHandler(info=Info(title='BlackSheep', version='0.0.1'))
docs.bind_app(app=app)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.app_host,
        port=int(settings.app_port),
        log_level=settings.log_level,
        reload=settings.reload,
    )
