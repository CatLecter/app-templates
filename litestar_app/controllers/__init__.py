from litestar.types import ControllerRouterHandler

from controllers.users import UserController

routes: list[ControllerRouterHandler] = [
    UserController,
]

__all__ = ['routes']
