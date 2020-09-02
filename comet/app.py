from starlette.applications import Starlette, BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles

from .global_state import GlobalStateMiddleware


class Comet(Starlette):
    def __init__(self):
        super().__init__()

        self.add_middleware(GlobalStateMiddleware)

    def add_static_folder(self, path: str, directory: str, name=None, **kwargs):
        self.mount(path, StaticFiles(directory=directory, **kwargs), name)
