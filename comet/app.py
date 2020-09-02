from starlette.applications import Starlette, BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware

from .global_state import GlobalStateMiddleware
from .minification import install_html_minification_hooks


class Comet(Starlette):
    def __init__(self):
        super().__init__(middleware=[Middleware(GlobalStateMiddleware)])

    def minify_html(self, **config):
        install_html_minification_hooks(**config)

    def add_static_folder(
        self, directory: str, path: str = None, name: str = None, **kwargs
    ):
        if path is None:
            path = "/" + directory

        self.mount(path, StaticFiles(directory=directory, **kwargs), name)
