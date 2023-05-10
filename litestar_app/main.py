import uvicorn
from litestar import Litestar

from controllers import UserController

app = Litestar(route_handlers=[UserController])

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=5000, log_level='debug', reload=True)
