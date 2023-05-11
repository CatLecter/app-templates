import uvicorn
from litestar import Litestar

from controllers import routes

app = Litestar(route_handlers=[*routes])

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=5000, log_level='debug', reload=True)
