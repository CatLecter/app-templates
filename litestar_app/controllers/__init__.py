from controllers.users import UserController
from litestar.types import ControllerRouterHandler

routes: list[ControllerRouterHandler] = [
    UserController,
]

__all__ = ['routes']
