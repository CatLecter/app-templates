import uvicorn
from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from controllers import UserController  # noqa
from db.postgres import PostgresDB

app = Application()
app.services.add_exact_scoped(PostgresDB)

docs = OpenAPIHandler(info=Info(title='BlackSheep API', version='0.0.1'))
docs.bind_app(app=app)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='debug', reload=True)
