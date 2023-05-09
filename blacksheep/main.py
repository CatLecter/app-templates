import uvicorn
from controllers import UserController  # noqa

from blacksheep import Application

app = Application()

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000, log_level='debug')
