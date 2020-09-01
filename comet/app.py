from typing import Callable, List
from starlette.applications import Starlette, BaseHTTPMiddleware

from .global_state import GlobalStateMiddleware


class Comet(Starlette):
    def __init__(self):
        super().__init__()

        self.add_middleware(GlobalStateMiddleware)
